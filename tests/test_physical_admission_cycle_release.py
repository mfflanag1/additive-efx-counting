"""Physical cycle-release coverage, counterchecks, and independent Fraction oracle."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from fractions import Fraction
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tracks/physical_admission/verify_cycle_release.py"
ARCHIVE = ROOT / "results/selector_compatibility_4x9_exact_audit_20261016.json"
SPEC = importlib.util.spec_from_file_location("physical_admission_cycle_release", SCRIPT)
release = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release
SPEC.loader.exec_module(release)


def document(values, owners):
    return {"schema": release.INPUT_SCHEMA, "n": 4, "m": len(owners),
            "agent_order": [0, 1, 2, 3], "values": values,
            "candidate": {"base_owner": owners}}


def calibration():
    return release.load_instance(ARCHIVE, archive=True)


def calibration_edges():
    return [{"source": 1, "target": 3, "goods": [5]},
            {"source": 3, "target": 2, "goods": [4, 8]},
            {"source": 2, "target": 1, "goods": [2, 3, 8]}]


def positive_control():
    # Safe EFX, deliberately not globally maximal: the canonical GG probe is EFX.
    return release.parse_instance(document(
        [[3, 4, 3, 9, "1/2", 11, 1, 2],
         [4, 5, "1/2", 7, 3, 1, 1, 2],
         [3, 3, 1, 1, 7, 9, 10, 1],
         [1, 1, "1/2", 1, 1, 1, 3, 1]],
        [0, 0, 0, 1, 1, 2, 3, None]))


def independent_fraction_oracle(instance, owners):
    """No implementation arithmetic, bundles, tails or deletion reports are reused."""
    rows = [[Fraction(v, instance.denominator) for v in row] for row in instance.values_scaled]
    bundles = [{g for g in range(instance.m) if owners[g] == i} for i in range(4)]
    own = [sum((rows[i][g] for g in bundles[i]), Fraction(0)) for i in range(4)]
    comparisons = {}
    for observer in range(4):
        for target in range(4):
            for deleted in bundles[target]:
                rhs = sum((rows[observer][g] for g in bundles[target] - {deleted}), Fraction(0))
                comparisons[observer, target, deleted] = own[observer] - rhs
    tails = [[max([sum((rows[i][g] for g in bundle - {h}), Fraction(0)) for h in bundle] + [Fraction(0)])
              for bundle in bundles] for i in range(4)]
    return own, comparisons, tails


class CycleReleaseTests(unittest.TestCase):
    def test_calibration_canonical_cycle_and_both_priority_winners(self):
        report = release.audit(calibration())
        self.assertEqual(report["status"], "verified_instance")
        self.assertEqual(report["exhaustive_coverage"]["decorated_cycle_count"], 1)
        self.assertEqual(report["canonical_cycle"]["vertices"], [1, 3, 2])
        self.assertEqual(report["canonical_cycle"]["p_edge_count"], 2)
        self.assertEqual(report["priority_compatible_winners"], [2, 3])
        expected = {2: [[6, 7], [5], [2, 3, 8], [4]],
                    3: [[6, 7], [5], [2, 3], [4, 8]]}
        for probe in report["probes"]:
            winner = probe["winner"]
            self.assertEqual(probe["bundles"], expected[winner])
            self.assertEqual(probe["charity"], [0, 1])
            self.assertEqual(probe["base_owner"][8], winner)
            self.assertEqual(probe["unpaid_sources"], [5 - winner])
            self.assertTrue(probe["fixed_priority_lexicographic_improvement"])
            self.assertFalse(probe["is_efx"])
            self.assertEqual(probe["outcome"], "unpaid_observer_obstruction")
            self.assertEqual({v["observer"] for v in probe["efx_violations"]}, {5 - winner})
            self.assertEqual({v["target"] for v in probe["efx_violations"]}, {0})
            self.assertEqual({v["target_kind"] for v in probe["efx_violations"]}, {"external_fixed"})

    def test_raw_source_deficits_are_not_physical_tail_deficits_or_role_deletions(self):
        report = release.audit(calibration())
        expected = {2: (3, 2064, 1072), 3: (2, 4101, 3124)}
        for probe in report["probes"]:
            source, raw, tail = expected[probe["winner"]]
            self.assertEqual(probe["source_deficits"][0]["source"], source)
            self.assertEqual(probe["source_deficits"][0]["deficit_scaled"], raw)
            self.assertEqual(probe["tail_deficits"][0]["tail_deficit_scaled"], tail)
            self.assertNotEqual(raw, tail)
            violation, = probe["efx_violations"]
            self.assertEqual(violation["deleted_good"], 7)
            self.assertEqual(violation["shortfall_scaled"], tail)
            # Deleting all of a bundled "role" {6,7} would falsely erase this wall.
            self.assertGreater(violation["rhs_scaled"], 0)
            self.assertLessEqual(tail, raw)
            self.assertLess(raw, violation["p_value_scaled"])

    def test_every_physical_deletion_matches_independent_fraction_oracle(self):
        original = calibration()
        instance = release.Instance(original.values_scaled, 7, original.base_owner)
        report = release.audit(instance)
        for probe in report["probes"]:
            own, slacks, tails = independent_fraction_oracle(instance, probe["base_owner"])
            actual = {(item["observer"], item["target"], item["deleted_good"]):
                      Fraction(item["slack_scaled"], 7) for item in probe["efx_comparisons"]}
            self.assertEqual(actual, slacks)
            self.assertEqual([str(value) for value in own], probe["utilities_exact"])
            failures = {key for key, slack in slacks.items() if slack < 0}
            self.assertEqual(failures, {(v["observer"], v["target"], v["deleted_good"])
                                        for v in probe["efx_violations"]})
            source = probe["unpaid_sources"][0]
            self.assertEqual(Fraction(probe["tail_deficits"][0]["tail_deficit_exact"]),
                             max(Fraction(0), max(tails[source]) - own[source]))

    def test_probe_verifier_does_not_use_extractor_allocation_record(self):
        instance = calibration()
        with patch.object(release.extractor, "allocation_record", side_effect=AssertionError("not independent")):
            probe = release.construct_cycle_release_probe(instance, calibration_edges(), 2)
        self.assertEqual(probe["tail_deficits"][0]["tail_deficit_scaled"], 1072)

    def test_positive_control_reports_genuine_improvement_not_universal_theorem(self):
        report = release.audit(positive_control())
        self.assertEqual(report["status"], "verified_instance")
        self.assertEqual(report["canonical_cycle"]["vertices"], [0, 1])
        self.assertEqual(report["priority_compatible_winners"], [0])
        probe, = report["probes"]
        self.assertEqual(probe["bundles"], [[3, 7], [0, 1], [5], [6]])
        self.assertEqual(probe["charity"], [2, 4])
        self.assertTrue(probe["is_efx"])
        self.assertEqual(probe["outcome"], "genuine_efx_lex_improvement")
        self.assertTrue(probe["excluded_if_input_is_global_lexmax"])
        self.assertEqual(probe["efx_violations"], [])
        self.assertEqual(probe["tail_deficits"][0]["tail_deficit_scaled"], 0)
        for key in ("global_lexmax_verified", "universal_gg_claimed", "admit4_claimed",
                    "universal_admission_theorem_verified"):
            self.assertFalse(report["claims_boundary"][key])

    def test_earliest_p_source_must_win_even_if_other_winner_is_physically_possible(self):
        instance = positive_control()
        edges = release.audit(instance)["canonical_cycle"]["edges"]
        with self.assertRaisesRegex(ValueError, "priority-compatible.*SOURCE"):
            release.construct_cycle_release_probe(instance, edges, 1)

    def test_wrong_winner_orientation_and_non_p_winner_rejected(self):
        for winner in (0, 1, True, 4, None):
            with self.subTest(winner=winner), self.assertRaisesRegex(ValueError, "SOURCE"):
                release.construct_cycle_release_probe(calibration(), calibration_edges(), winner)
        # Receiving a core goes to the edge's source, not to its target.
        wrong = [2, None, 1, 1, 2, 3, 0, 0, 1]
        with self.assertRaisesRegex(ValueError, "ownership disagrees"):
            release.construct_cycle_release_probe(calibration(), calibration_edges(), 2, claimed_owners=wrong)

    def test_nonphysical_core_and_forged_core_metadata_rejected(self):
        bad = deepcopy(calibration_edges())
        bad[1]["goods"] = [4, 6, 8]
        bad[1]["champions"] = [3]
        bad[1]["common_safe"] = True
        with self.assertRaisesRegex(ValueError, "nonphysical core"):
            release.validate_cycle(calibration(), bad)
        for goods in ([4, 4, 8], [4, True, 8], [4, 9], [], [4, "8"]):
            bad = deepcopy(calibration_edges())
            bad[1]["goods"] = goods
            with self.subTest(goods=goods), self.assertRaises(ValueError):
                release.validate_cycle(calibration(), bad)

    def test_nonstrict_champion_and_unsafe_core_rejected(self):
        bad = deepcopy(calibration_edges())
        bad[0]["source"] = 0
        with self.assertRaisesRegex(ValueError, "strict champion"):
            release.validate_cycle(calibration(), bad)
        original = calibration()
        rows = [list(row) for row in original.values_scaled]
        # Base unchanged and EFX, but deletion of 4 from {4,8} exceeds observer 0's floor.
        rows[0][8] = rows[0][6] + rows[0][7] + 1
        instance = release.Instance(tuple(tuple(row) for row in rows), 1, original.base_owner)
        with self.assertRaisesRegex(ValueError, "not safe"):
            release.validate_cycle(instance, calibration_edges())
        rows = [list(row) for row in original.values_scaled]
        rows[0][2] = 10300  # O stays EFX, but deleting 3 from {2,3,8} is unsafe.
        instance = release.Instance(tuple(tuple(row) for row in rows), 1, original.base_owner)
        with self.assertRaisesRegex(ValueError, "not common-safe"):
            release.validate_cycle(instance, calibration_edges())

    def test_proper_retained_part_full_ordinary_core_and_cycle_order_required(self):
        bad = deepcopy(calibration_edges())
        bad[1]["goods"] = [0, 4, 8]
        with self.assertRaisesRegex(ValueError, "nonempty proper"):
            release.validate_cycle(calibration(), bad)
        bad[1]["goods"] = [8]
        with self.assertRaisesRegex(ValueError, "nonempty proper"):
            release.validate_cycle(calibration(), bad)
        bad[1]["goods"] = [4]
        with self.assertRaisesRegex(ValueError, "whole old target"):
            release.validate_cycle(calibration(), bad)
        with self.assertRaisesRegex(ValueError, "source-to-target"):
            release.validate_cycle(calibration(), calibration_edges()[::-1])
        with self.assertRaises(ValueError):
            release.validate_cycle(calibration(), calibration_edges()[:1])

    def test_weak_zero_source_deficit_allowed_without_nondegeneracy(self):
        original = calibration()
        rows = [list(row) for row in original.values_scaled]
        rows[3][5] = rows[3][4]
        rows[3][6] = 17000
        instance = release.Instance(tuple(tuple(row) for row in rows), 1, original.base_owner)
        probe = release.construct_cycle_release_probe(instance, calibration_edges(), 2)
        self.assertEqual(probe["source_deficits"][0]["deficit_scaled"], 0)
        self.assertFalse(probe["source_deficits"][0]["lower_bound_is_strict"])
        self.assertEqual(probe["efx_violations"], [])

    def test_corrupt_physical_ownership_is_detected(self):
        expected = release.construct_cycle_release_probe(calibration(), calibration_edges(), 2)["base_owner"]
        for owners in (expected[:-1], [True] + expected[1:], expected[:-1] + [None]):
            with self.subTest(owners=owners), self.assertRaises(ValueError):
                release.construct_cycle_release_probe(calibration(), calibration_edges(), 2, claimed_owners=owners)
        self.assertEqual(release.construct_cycle_release_probe(calibration(), calibration_edges(), 2,
                         claimed_owners=expected)["base_owner"], expected)

    def test_archive_global_claims_and_complete_exits_are_ignored(self):
        data = json.loads(ARCHIVE.read_text())
        baseline = release.audit(release.parse_instance(data, archive=True))
        data["candidate"]["attains_domain_maximum"] = {"all_partial_efx": "fabricated"}
        data["domains"] = {"complete_efx": "no exits"}
        data["complete_exits"] = [{"not_a_physical_allocation": True}]
        self.assertEqual(release.audit(release.parse_instance(data, archive=True)), baseline)
        data["candidate"]["utilities_scaled"][0] += 1
        with self.assertRaisesRegex(ValueError, "utilities_scaled"):
            release.parse_instance(data, archive=True)

    def test_not_applicable_does_not_skip_shorter_cycle_for_favorable_probe(self):
        instance = release.parse_instance(document([[1] * 5 for _ in range(4)], [0, 1, 2, 3, None]))
        report = release.audit(instance)
        self.assertGreater(report["exhaustive_coverage"]["decorated_cycle_count"], 1)
        self.assertEqual(report["canonical_cycle"]["vertices"], [0])
        self.assertEqual(report["status"], "not_applicable")
        self.assertEqual(report["probes"], [])
        self.assertFalse(report["claims_boundary"]["universal_admission_theorem_verified"])

    def test_enumeration_bounds_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "max_goods"):
            release.load_instance(ARCHIVE, archive=True, max_goods=8)
        instance = release.parse_instance(document([[1] * 5 for _ in range(4)], [0, 1, 2, 3, None]))
        with self.assertRaisesRegex(ValueError, "decorated cycles exceed"):
            release.audit(instance, max_decorated_cycles=1)

    def test_corrupt_internal_chord_or_parallel_ordinary_envy_fails_closed(self):
        instance = calibration()
        coverage = release.extractor.audit(instance)
        coverage["champion_records"].append({"source": 1, "target": 2, "goods": [4, 8], "core_id": 99})
        with patch.object(release.extractor, "audit", return_value=coverage):
            with self.assertRaisesRegex(RuntimeError, "internal non-successor"):
                release.audit(instance)
        original = calibration()
        rows = [list(row) for row in original.values_scaled]
        rows[3][5] = rows[3][4]
        rows[3][6] = 17000
        instance = release.Instance(tuple(tuple(row) for row in rows), 1, original.base_owner)
        coverage = release.extractor.audit(original)
        with patch.object(release.extractor, "audit", return_value=coverage):
            with self.assertRaisesRegex(RuntimeError, "parallel ordinary envy"):
                release.audit(instance)

    def test_residual_return_complete_paid_but_not_efx_calibration(self):
        report = release.audit(calibration())
        returned = report["residual_return"]
        self.assertEqual(returned["ordinary_run_count"], 1)
        self.assertEqual(returned["return_compatible_winners"], [3])
        self.assertEqual(report["priority_compatible_winners"], [2, 3])
        probe, = returned["probes"]
        self.assertEqual(probe["bundles"], [[6, 7], [1, 5], [0, 2, 3], [4, 8]])
        self.assertEqual(probe["charity"], [])
        self.assertEqual(probe["utilities_scaled"], [10432, 38946, 36877, 22800])
        self.assertEqual(probe["junction_targets"], [1, 2])
        self.assertTrue(probe["complete"])
        self.assertTrue(probe["strict_for_every_participant"])
        self.assertTrue(probe["is_pareto_improvement"])
        self.assertFalse(probe["is_efx"])
        self.assertFalse(probe["excluded_if_input_is_global_lexmax"])
        self.assertFalse(probe["unconditional_complete_efx_claimed"])
        self.assertEqual(probe["outcome"], "augmented_junction_obstruction")
        failure, = probe["efx_violations"]
        self.assertEqual(failure, {"observer": 1, "target": 2, "deleted_good": 3,
                                  "lhs_scaled": 38946, "rhs_scaled": 40965, "slack_scaled": -2019,
                                  "target_kind": "augmented_junction", "shortfall_scaled": 2019})
        self.assertTrue(probe["old_floor_common_safety_violations"])
        self.assertTrue(all(item["target"] in [1, 2] for item in probe["old_floor_common_safety_violations"]))
        with self.assertRaisesRegex(ValueError, "not return-compatible"):
            release.construct_cycle_return_probe(calibration(), calibration_edges(), 2)

    def test_all_g_return_allows_winners_not_compatible_with_release_priority(self):
        instance = positive_control()
        report = release.audit(instance)
        self.assertEqual(report["priority_compatible_winners"], [0])
        self.assertEqual(report["residual_return"]["ordinary_run_count"], 0)
        self.assertEqual(report["residual_return"]["return_compatible_winners"], [0, 1])
        for probe in report["residual_return"]["probes"]:
            self.assertTrue(probe["complete"])
            self.assertTrue(probe["strict_for_every_participant"])
            self.assertTrue(probe["is_pareto_improvement"])
            self.assertEqual(probe["base_owner"][2], 0)
            self.assertEqual(probe["base_owner"][4], 1)
            self.assertEqual(probe["base_owner"][7], probe["winner"])
            own, slacks, _ = independent_fraction_oracle(instance, probe["base_owner"])
            self.assertEqual(probe["utilities_exact"], [str(value) for value in own])
            self.assertEqual({(item["observer"], item["target"], item["deleted_good"]):
                              Fraction(item["slack_scaled"], instance.denominator)
                              for item in probe["efx_comparisons"]}, slacks)
            self.assertEqual({key for key, slack in slacks.items() if slack < 0},
                             {(item["observer"], item["target"], item["deleted_good"])
                              for item in probe["efx_violations"]})
            if probe["winner"] == 1:
                # The winner's augmented junction contains p too. Checking only
                # its p-free cross-pool would omit these physical failures.
                self.assertEqual(probe["bundles"][1], [0, 1, 4, 7])
                self.assertEqual({key for key, slack in slacks.items() if slack < 0},
                                 {(2, 1, 0), (2, 1, 1), (2, 1, 7)})

    def test_two_ordinary_runs_do_not_claim_all_paid_mechanism(self):
        # A four-cycle with alternating G,E,G,E decorations, not a search result.
        instance = release.parse_instance(document(
            [[10, 9, "1/2", 1, 1, 1, 2], [1, 5, 5, 11, 1, 1, 2],
             [1, 1, 1, 10, 9, "1/2", 2], [11, 1, 1, 1, 5, 5, 2]],
            [0, 1, 1, 2, 3, 3, None]))
        report = release.audit(instance)
        self.assertEqual(report["canonical_cycle"]["vertices"], [0, 1, 2, 3])
        self.assertEqual(report["residual_return"]["ordinary_run_count"], 2)
        self.assertEqual(report["residual_return"]["status"], "mechanism_not_guaranteed")
        self.assertEqual(report["residual_return"]["probes"], [])
        with self.assertRaisesRegex(ValueError, "mechanism_not_guaranteed"):
            release.construct_cycle_return_probe(instance, report["canonical_cycle"]["edges"], 0)

    def test_return_values_and_every_deletion_independently_checked_as_fractions(self):
        original = calibration()
        instance = release.Instance(original.values_scaled, 11, original.base_owner)
        with patch.object(release.extractor, "allocation_record", side_effect=AssertionError("not independent")):
            probe = release.construct_cycle_return_probe(instance, calibration_edges(), 3)
        own, slacks, _ = independent_fraction_oracle(instance, probe["base_owner"])
        self.assertEqual(probe["utilities_exact"], [str(value) for value in own])
        self.assertEqual({(item["observer"], item["target"], item["deleted_good"]):
                          Fraction(item["slack_scaled"], 11) for item in probe["efx_comparisons"]}, slacks)
        self.assertEqual({key for key, slack in slacks.items() if slack < 0},
                         {(item["observer"], item["target"], item["deleted_good"])
                          for item in probe["efx_violations"]})
        corrupted = list(probe["base_owner"])
        corrupted[1] = 2
        with self.assertRaisesRegex(ValueError, "ownership disagrees"):
            release.construct_cycle_return_probe(instance, calibration_edges(), 3, claimed_owners=corrupted)

    def test_cli_output_is_deterministic_and_errors_have_no_partial_json(self):
        outputs = []
        for _ in range(2):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(release.main([str(ARCHIVE), "--archive"]), 0)
            outputs.append(output.getvalue())
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], (ROOT / "results/physical_cycle_release_20261016.json").read_text())
        self.assertEqual(json.loads(outputs[0])["schema"], release.OUTPUT_SCHEMA)
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            self.assertEqual(release.main([str(ARCHIVE), "--archive", "--max-goods", "8"]), 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("rejected input", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
