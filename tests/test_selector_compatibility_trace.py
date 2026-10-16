"""Exact endpoint-certificate checks independent of the exhaustive enumerator."""

from contextlib import redirect_stdout
from copy import deepcopy
from fractions import Fraction
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "tracks/selector_compatibility/verify_trace.py"
SPEC = importlib.util.spec_from_file_location("independent_selector_trace", SCRIPT)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def perturb(rows):
    """For these m<10 fixtures, the binary tail separates every bundle sum."""
    return [[str(Fraction(1024 * value + 2 ** good, 3)) for good, value in enumerate(row)]
            for row in rows]


def pool_fixture():
    return {
        "schema": verifier.INPUT_SCHEMA,
        "values": perturb([[3, 4, 1, 1, 1], [1, 3, 1, 1, 2],
                           [1, 1, 3, 1, 1], [1, 1, 1, 3, 1]]),
        "priority": [0, 1, 2, 3],
        "base_owner": [0, 1, 2, 3, None],
        "exit_owner": [1, 0, 2, 3, None],
        "repair_steps": [{"rule": "pool_replacement", "owner": [None, 0, 2, 3, 1],
                          "recipient": 1, "desired_goods": [4]}],
        "outcome": "restricted_improvement",
    }


def mixed_fixture():
    data = pool_fixture()
    data["exit_owner"] = [None, 0, 2, 3, None]
    data["repair_steps"].insert(0, {"rule": "bcff_progress", "owner": [1, 0, 2, 3, None]})
    return data


def bcff_fixture():
    data = mixed_fixture()
    data["values"][1] = perturb([[4, 3, 1, 1, 1]])[0]
    data["repair_steps"].pop()
    return data


def complete_fixture():
    return {
        "schema": verifier.INPUT_SCHEMA,
        "values": perturb([[9, 1, 1, 1], [1, 3, 1, 1], [1, 1, 3, 1], [1, 1, 1, 3]]),
        "priority": [0, 1, 2, 3], "base_owner": [0, 1, 2, 3],
        "exit_owner": [1, 0, 2, 3], "repair_steps": [], "outcome": "complete",
    }


class ExactTraceTests(unittest.TestCase):
    def rejects(self, data, pattern=None, **kwargs):
        if pattern is None:
            with self.assertRaises(verifier.TraceValidationError):
                verifier.verify_trace(data, **kwargs)
        else:
            with self.assertRaisesRegex(verifier.TraceValidationError, pattern):
                verifier.verify_trace(data, **kwargs)

    def test_complete_efx_utility_loss_is_terminal(self):
        report = verifier.verify_trace(complete_fixture())
        self.assertTrue(report["valid"])
        self.assertTrue(report["original_exit_complete"])
        self.assertEqual(report["outcome"], "complete")
        self.assertLess(Fraction(report["exit"]["priority_utilities"][0]),
                        Fraction(report["base"]["priority_utilities"][0]))
        self.assertFalse(report["trust_boundary"]["universal_theorem_proved_by_this_check"])

    def test_complete_efx_equality_is_also_terminal(self):
        data = complete_fixture()
        data["exit_owner"] = data["base_owner"].copy()
        self.assertTrue(verifier.verify_trace(data)["valid"])

    def test_empty_good_set_is_complete_and_vacuously_nondegenerate(self):
        data = complete_fixture()
        data.update(values=[[], [], [], []], base_owner=[], exit_owner=[])
        report = verifier.verify_trace(data)
        self.assertTrue(report["bundle_nondegeneracy"]["all_agents"])
        self.assertTrue(report["valid"])

    def test_positive_exact_integer_and_rational_string_values(self):
        data = complete_fixture()
        data["values"] = [[int(Fraction(value) * 3) for value in row] for row in data["values"]]
        self.assertTrue(verifier.verify_trace(data)["valid"])
        self.assertTrue(verifier.verify_trace(complete_fixture())["valid"])

    def test_direct_restricted_improvement_needs_no_trace(self):
        data = bcff_fixture()
        data["exit_owner"] = data["repair_steps"].pop()["owner"]
        report = verifier.verify_trace(data)
        self.assertEqual(report["repair_step_count"], 0)
        self.assertTrue(report["exit"]["in_restricted_class"])

    def test_bcff_repairs_efx_exit_with_two_charity_goods(self):
        report = verifier.verify_trace(bcff_fixture())
        self.assertTrue(report["exit"]["is_efx"])
        self.assertFalse(report["exit"]["in_restricted_class"])
        self.assertEqual(len(report["exit"]["charity"]), 2)
        self.assertEqual(report["repair_step_count"], 1)
        self.assertTrue(report["final"]["in_restricted_class"])
        self.assertTrue(report["within_frozen_scope"])

    def test_bcff_lex_progress_can_lower_a_later_priority_utility(self):
        data = bcff_fixture()
        # Agent 1 improves from empty while later-priority agent 3 loses its
        # singleton. The subsequent step restores agent 3 and reaches S.
        data["repair_steps"].insert(0, {"rule": "bcff_progress", "owner": [1, 0, 2, None, None]})
        report = verifier.verify_trace(data)
        before, after = report["exit"], report["repair_steps"][0]["endpoint"]
        self.assertGreater(Fraction(after["own_utilities"][1]), Fraction(before["own_utilities"][1]))
        self.assertLess(Fraction(after["own_utilities"][3]), Fraction(before["own_utilities"][3]))
        self.assertTrue(report["valid"])

    def test_pool_repairs_unsafe_singleton_with_exact_replacement(self):
        report = verifier.verify_trace(pool_fixture())
        self.assertFalse(report["exit"]["charity_safe"])
        self.assertEqual(report["repair_steps"][0]["recipient"], 1)
        self.assertEqual(report["repair_steps"][0]["desired_goods"], [4])
        self.assertEqual(report["final"]["charity"], [0])
        for i in (0, 2, 3):
            self.assertEqual(report["exit"]["bundles"][i], report["final"]["bundles"][i])

    def test_pool_metadata_can_be_omitted_and_is_inferred(self):
        data = pool_fixture()
        data["repair_steps"][0].pop("recipient")
        data["repair_steps"][0].pop("desired_goods")
        self.assertTrue(verifier.verify_trace(data)["valid"])

    def test_mixed_trace_may_remain_unsafe_after_bcff(self):
        report = verifier.verify_trace(mixed_fixture())
        self.assertEqual(report["repair_step_count"], 2)
        intermediate = report["repair_steps"][0]["endpoint"]
        self.assertTrue(intermediate["is_efx"])
        self.assertFalse(intermediate["charity_safe"])

    def test_any_fixed_permutation_supported_but_its_sign_matters(self):
        data = mixed_fixture()
        data["priority"] = [2, 3, 0, 1]
        self.assertTrue(verifier.verify_trace(data)["valid"])
        data["priority"] = [1, 0, 2, 3]
        self.rejects(data, "partial exit must strictly improve")

    def test_complete_after_repair_has_complete_outcome(self):
        data = bcff_fixture()
        # Give the remaining low-value good to agent 0: its other good is
        # observed as low by everyone else, so every EFX deletion still passes.
        data["repair_steps"][0]["owner"] = [1, 0, 2, 3, 0]
        data["outcome"] = "complete"
        report = verifier.verify_trace(data)
        self.assertFalse(report["original_exit_complete"])
        self.assertTrue(report["final"]["complete"])

    def test_complete_repair_endpoint_cannot_bypass_strict_progress(self):
        data = bcff_fixture()
        data["repair_steps"][0]["owner"] = [0, 1, 2, 3, 3]
        data["outcome"] = "complete"
        self.rejects(data, "successor must strictly improve")

    def test_nondegeneracy_default_rejects_ties_and_reports_collision(self):
        data = complete_fixture()
        data["values"] = [[1, 1, 1, 1]] * 4
        with self.assertRaisesRegex(verifier.TraceValidationError, "bundle-nondegenerate") as caught:
            verifier.verify_trace(data)
        report = caught.exception.report
        self.assertFalse(report["bundle_nondegeneracy"]["all_agents"])
        self.assertEqual(report["bundle_nondegeneracy"]["agents"][0]["collision"]["value"], "1")

    def test_subset_sum_collision_detected_even_without_equal_items(self):
        data = complete_fixture()
        data["values"] = [[1, 2, 3, 8]] * 4
        self.rejects(data, "bundle-nondegenerate")

    def test_default_size_guard_precedes_exponential_checks(self):
        self.assertEqual(verifier.DEFAULT_MAX_GOODS, 16)
        data = complete_fixture()
        data.update(values=[[2 ** g for g in range(17)]] * 4,
                    base_owner=[None] * 17, exit_owner=[None] * 17)
        with patch.object(verifier, "_nondegeneracy") as nondegeneracy:
            self.rejects(data, "17 goods exceed max_goods=16")
            nondegeneracy.assert_not_called()
        with patch.object(verifier, "_pool_replacement") as pool_check:
            with self.assertRaisesRegex(verifier.TraceValidationError, "17 goods exceed max_goods=16"):
                verifier.check_pool_replacement(data["values"], data["base_owner"], data["exit_owner"])
            pool_check.assert_not_called()

    def test_explicit_positive_size_bound_and_override(self):
        data = complete_fixture()
        self.rejects(data, "4 goods exceed max_goods=3", max_goods=3)
        self.assertTrue(verifier.verify_trace(data, max_goods=4)["valid"])
        pool = pool_fixture()
        with self.assertRaisesRegex(verifier.TraceValidationError, "5 goods exceed max_goods=4"):
            verifier.check_pool_replacement(pool["values"], pool["exit_owner"], pool["repair_steps"][0]["owner"],
                                            max_goods=4)
        self.assertEqual(verifier.check_pool_replacement(
            pool["values"], pool["exit_owner"], pool["repair_steps"][0]["owner"], max_goods=5)["recipient"], 1)
        for invalid in (True, False, 0, -1, 4.0, "4", None):
            with self.subTest(max_goods=invalid):
                self.rejects(data, "max_goods must be a positive integer", max_goods=invalid)
                with self.assertRaisesRegex(verifier.TraceValidationError, "max_goods must be a positive integer"):
                    verifier.check_pool_replacement(pool["values"], pool["exit_owner"],
                                                    pool["repair_steps"][0]["owner"], max_goods=invalid)

    def test_degenerate_pool_calibration_is_explicitly_outside_frozen_scope(self):
        data = pool_fixture()
        data["values"] = [[3, 4, 1, 1, 1], [1, 3, 1, 1, 2],
                          [1, 1, 3, 1, 1], [1, 1, 1, 3, 1]]
        self.rejects(data, "bundle-nondegenerate")
        report = verifier.verify_trace(data, require_nondegenerate=False)
        self.assertTrue(report["valid"])
        self.assertFalse(report["within_frozen_scope"])
        self.assertFalse(report["nondegeneracy_required"])

    def test_degenerate_bcff_is_rejected_even_in_relaxed_mode(self):
        data = bcff_fixture()
        data["values"] = [[3, 4, 1, 1, 1], [4, 3, 1, 1, 1],
                          [1, 1, 3, 1, 1], [1, 1, 1, 3, 1]]
        self.rejects(data, "BCFF progress requires bundle-nondegenerate", require_nondegenerate=False)

    def test_complete_non_efx_all_good_reset_rejected(self):
        data = complete_fixture()
        for owner in range(4):
            data["exit_owner"] = [owner] * 4
            with self.subTest(owner=owner):
                self.rejects(data, "exit must be EFX")

    def test_partial_non_efx_exit_rejected(self):
        data = pool_fixture()
        data["exit_owner"] = [0, 0, None, 3, None]
        self.rejects(data, "exit must be EFX")

    def test_base_must_be_efx_safe_and_have_small_charity(self):
        for owner in ([0, 0, 0, 0, None], [None, None, 2, 3, None], [1, 0, 2, 3, None]):
            data = pool_fixture()
            data["base_owner"] = owner
            with self.subTest(owner=owner):
                self.rejects(data, "base must be EFX, charity-safe")

    def test_partial_equality_is_not_an_improving_exit(self):
        data = pool_fixture()
        data["exit_owner"] = data["base_owner"].copy()
        data["repair_steps"] = []
        self.rejects(data, "partial exit must strictly improve")

    def test_non_strict_and_non_efx_bcff_steps_rejected(self):
        data = bcff_fixture()
        data["repair_steps"][0]["owner"] = data["exit_owner"].copy()
        self.rejects(data, "successor must strictly improve")
        data["repair_steps"][0]["owner"] = [0, 0, 2, 3, None]
        self.rejects(data, "successor must be EFX")

    def test_rule_priority_is_enforced_in_both_directions(self):
        data = bcff_fixture()
        data["repair_steps"][0]["rule"] = "pool_replacement"
        self.rejects(data, "BCFF has rule priority")
        data = pool_fixture()
        data["repair_steps"][0] = {"rule": "bcff_progress", "owner": [None, 0, 2, 3, 1]}
        self.rejects(data, "at least two unallocated goods")

    def test_no_empty_or_unfinished_repair_for_out_of_class_exit(self):
        data = mixed_fixture()
        data["repair_steps"].pop()
        self.rejects(data, "repair trace must end in S")
        data["repair_steps"] = []
        self.rejects(data, "repair trace must end in S")

    def test_stop_at_first_s_and_no_trace_after_complete_exit(self):
        data = bcff_fixture()
        data["repair_steps"].append(deepcopy(data["repair_steps"][0]))
        self.rejects(data, "trace must stop at the first state in S")
        data = complete_fixture()
        data["repair_steps"] = [{"rule": "bcff_progress", "owner": data["exit_owner"]}]
        self.rejects(data, "complete EFX exits require an empty repair trace")

    def test_pool_replacement_metadata_and_unrelated_changes_rejected(self):
        for field, value in (("recipient", True), ("recipient", 0), ("recipient", 4),
                             ("desired_goods", [True]), ("desired_goods", [4, 4]),
                             ("desired_goods", [0]), ("desired_goods", [5]),
                             ("desired_goods", "4"), ("owner", [None, 2, 0, 3, 1]),
                             ("owner", [1, 0, 2, 3, 1])):
            data = pool_fixture()
            data["repair_steps"][0][field] = value
            with self.subTest(field=field, value=value):
                self.rejects(data)

    def test_pool_lemma_minimum_cardinality_checked_across_all_agents(self):
        values = [[3, 3, 3, 3, 2, 2]] * 4
        before, after = [0, 1, 2, 3, None, None], [None, 1, 2, 3, 0, 0]
        result = verifier.check_pool_replacement(values, before, after, recipient=0, desired_goods=[4, 5])
        self.assertEqual(result["minimum_cardinality_over_all_agents"], 2)
        values = deepcopy(values)
        values[1][1] = 1
        with self.assertRaisesRegex(verifier.TraceValidationError, "envied by any agent"):
            verifier.check_pool_replacement(values, before, after, recipient=0, desired_goods=[4, 5])

    def test_outcome_must_match_final_endpoint(self):
        data = complete_fixture()
        data["outcome"] = "restricted_improvement"
        self.rejects(data, "outcome must be complete")
        data = pool_fixture()
        data["outcome"] = "complete"
        self.rejects(data, "outcome must be restricted_improvement")

    def test_malformed_values_are_rejected(self):
        for value in (0, -1, "0/3", "1/0", "nan", True, False, 0.1, Fraction(1, 3), None, {}, []):
            data = complete_fixture()
            data["values"][0][0] = value
            with self.subTest(value=value):
                self.rejects(data)
        for values in ([], [[1]], [[1], [1], [1], [1, 2]], [1, 2, 3, 4]):
            data = complete_fixture()
            data["values"] = values
            with self.subTest(values=values):
                self.rejects(data)

    def test_missing_extra_and_changed_priority_fields_rejected(self):
        for field in complete_fixture():
            data = complete_fixture()
            del data[field]
            with self.subTest(missing=field):
                self.rejects(data, "missing required")
        for field, value in (("schema", "unknown"), ("priority", [0, 0, 2, 3]),
                             ("priority", [False, 1, 2, 3]), ("priority", [0, 1, 2]),
                             ("exit_priority", [1, 0, 2, 3]), ("bundles", [[0, 0], [], [], []]),
                             ("outcome", "other"), ("repair_steps", {})):
            data = complete_fixture()
            data[field] = value
            with self.subTest(field=field, value=value):
                self.rejects(data)
        for field in ("priority", "agent_order", "exit_priority"):
            data = pool_fixture()
            data["repair_steps"][0][field] = [1, 0, 2, 3]
            with self.subTest(field=field):
                self.rejects(data, "unsupported fields")

    def test_missing_cloned_or_invalid_owner_representations_rejected(self):
        for owner in ([0, 1, 2], [0, 1, 2, 3, None], [0, 1, 2, 4],
                      [0, 1, 2, True], [0, 1, 2, -1], [0, 1, 2, "3"],
                      [[0, 1], 1, 2, 3], {"0": 0}):
            for field in ("base_owner", "exit_owner"):
                data = complete_fixture()
                data[field] = owner
                with self.subTest(field=field, owner=owner):
                    self.rejects(data)
        data = pool_fixture()
        data["repair_steps"][0]["owner"] = [None, 0, 2, 3, 1, 1]
        self.rejects(data, "exactly one owner per original good")

    def test_bad_repair_step_schema_rejected(self):
        for step in (None, {}, {"rule": "unknown", "owner": [0, 1, 2, 3, None]},
                     {"rule": "bcff_progress", "owner": [1, 0, 2, 3, None], "recipient": 1}):
            data = bcff_fixture()
            data["repair_steps"] = [step]
            with self.subTest(step=step):
                self.rejects(data)

    def test_json_float_nonfinite_and_duplicate_keys_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            for text in ('{"values": 0.1}', '{"values": 1.0}', '{"values": NaN}',
                         '{"values": Infinity}', '{"schema":"a","schema":"b"}'):
                source.write_text(text)
                with self.subTest(text=text), self.assertRaises(ValueError):
                    verifier.load_document(source)

    def test_cli_deterministic_success_and_failure_does_not_clobber_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "input.json", Path(directory) / "report.json"
            source.write_text(json.dumps(mixed_fixture()))
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(verifier.main([str(source), "--output", str(target)]), 0)
            first = target.read_text()
            self.assertEqual(first, stdout.getvalue())
            with redirect_stdout(io.StringIO()):
                self.assertEqual(verifier.main([str(source), "--output", str(target)]), 0)
            self.assertEqual(first, target.read_text())
            data = mixed_fixture()
            data["exit_owner"] = [0, 0, 0, 0, 0]
            source.write_text(json.dumps(data))
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.assertEqual(verifier.main([str(source), "--output", str(target)]), 2)
            self.assertFalse(json.loads(stdout.getvalue())["valid"])
            self.assertEqual(first, target.read_text())
            original = source.read_text()
            with redirect_stdout(io.StringIO()):
                self.assertEqual(verifier.main([str(source), "--output", str(source)]), 2)
            self.assertEqual(original, source.read_text())

    def test_cli_explicit_size_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            source.write_text(json.dumps(complete_fixture()))
            for bound, expected in (("0", 2), ("3", 2), ("4", 0), ("17", 0)):
                stdout = io.StringIO()
                with self.subTest(bound=bound), redirect_stdout(stdout):
                    self.assertEqual(verifier.main([str(source), "--max-goods", bound]), expected)
                self.assertEqual(json.loads(stdout.getvalue())["valid"], expected == 0)


if __name__ == "__main__":
    unittest.main()
