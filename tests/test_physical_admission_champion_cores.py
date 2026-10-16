"""Exact physical-core extraction and independently checked cycle witnesses."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from fractions import Fraction
import importlib.util
import io
from itertools import combinations
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tracks/physical_admission/extract_champion_cores.py"
ARCHIVE = ROOT / "results/selector_compatibility_4x9_exact_audit_20261016.json"
SPEC = importlib.util.spec_from_file_location("physical_admission_champion_cores", SCRIPT)
cores = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cores
SPEC.loader.exec_module(cores)


def document(values, owners):
    return {"schema": cores.INPUT_SCHEMA, "n": 4, "m": len(owners),
            "agent_order": [0, 1, 2, 3], "values": values,
            "candidate": {"base_owner": owners}}


def uniform_instance():
    return cores.parse_instance(document([[1] * 5 for _ in range(4)], [0, 1, 2, 3, None]))


def multicores_instance():
    # All three two-good subsets of O_0 + p are minimal envied cores. The core
    # O_0 itself is tied (not strictly preferred) for agent 0, championed by 1..3.
    return cores.parse_instance(document([[2, 2, 3, 3, 3, 2] for _ in range(4)], [0, 0, 1, 2, 3, None]))


def independent_core_oracle(instance):
    """Test every proper subset, not the implementation's one-deletion shortcut."""
    values = [[Fraction(value, instance.denominator) for value in row] for row in instance.values_scaled]
    own = [sum(values[i][g] for g, owner in enumerate(instance.base_owner) if owner == i) for i in range(4)]
    result = set()
    for target in range(4):
        augmented = [g for g, owner in enumerate(instance.base_owner) if owner in (target, None)]
        for size in range(1, len(augmented) + 1):
            for goods in combinations(augmented, size):
                champions = tuple(i for i in range(4) if sum(values[i][g] for g in goods) > own[i])
                proper_subset_envied = any(sum(values[i][g] for g in subset) > own[i]
                                          for smaller in range(size) for subset in combinations(goods, smaller)
                                          for i in range(4))
                if champions and not proper_subset_envied:
                    result.add((target, goods, champions))
    return result


def independent_cycle_oracle(records):
    """DFS every edge-decorated cycle, canonicalized only by its least source."""
    signatures = set()
    for first in range(4):
        def visit(source, visited, chosen):
            for edge in records:
                if edge["source"] != source:
                    continue
                target = edge["target"]
                if target == first:
                    cycle = chosen + [edge]
                    signatures.add(tuple((item["source"], item["target"], item["core_id"]) for item in cycle))
                elif target > first and target not in visited:
                    visit(target, visited | {target}, chosen + [edge])
        visit(first, {first}, [])
    return signatures


class PhysicalChampionCoreTests(unittest.TestCase):
    def test_safe_nonmaximal_state_has_legal_self_improvements(self):
        instance = uniform_instance()
        report = cores.audit(instance)
        self.assertTrue(report["base_allocation"]["is_efx"])
        self.assertTrue(report["base_allocation"]["whole_charity_nonenvy"])
        self.assertEqual(report["summary"]["core_count"], 4)
        self.assertEqual(report["summary"]["champion_record_count"], 16)
        self.assertEqual(report["summary"]["decorated_cycle_count"], 24)
        self.assertEqual(report["summary"]["decorated_cycle_count_by_length"], {"1": 4, "2": 6, "3": 8, "4": 6})
        self.assertEqual(report["summary"]["decorated_self_loop_count"], 4)
        self.assertEqual(report["summary"]["disjoint_core_cycle_count"], 4)
        for cycle in report["decorated_cycles"]:
            if len(cycle["vertices"]) == 1:
                source = cycle["vertices"][0]
                exchange = cycle["exchange"]
                self.assertEqual(exchange["base_owner"][4], source)
                self.assertEqual(exchange["utility_gains_scaled"], [int(i == source) for i in range(4)])
                self.assertTrue(exchange["is_efx"])
                self.assertTrue(exchange["is_pareto_improvement"])
                self.assertTrue(exchange["strict_for_every_participant"])
                self.assertTrue(exchange["unchanged_nonparticipants"])
            else:
                self.assertFalse(cycle["cores_disjoint"])
                self.assertIsNone(cycle["exchange"])
        self.assertFalse(report["scope"]["global_lexmax_verified"])

    def test_overlap_in_charity_is_not_a_physical_exchange(self):
        edges = [{"source": 0, "target": 1, "goods": [1, 4]},
                 {"source": 1, "target": 0, "goods": [0, 4]}]
        with self.assertRaisesRegex(ValueError, "overlap"):
            cores.construct_cycle_exchange(uniform_instance(), edges)

    def test_all_multiple_cores_all_champions_and_exact_ties_are_retained(self):
        instance = multicores_instance()
        report = cores.audit(instance)
        actual = {(item["target"], tuple(item["goods"]), tuple(item["champions"])) for item in report["cores"]}
        self.assertEqual(actual, independent_core_oracle(instance))
        self.assertEqual(report["summary"]["core_count_by_target"], [3, 1, 1, 1])
        target_zero = [item for item in report["cores"] if item["target"] == 0]
        self.assertEqual([item["goods"] for item in target_zero], [[0, 1], [0, 5], [1, 5]])
        self.assertTrue(all(item["champions"] == [1, 2, 3] for item in target_zero))
        self.assertEqual(report["cores"][0]["values_scaled"][0], report["base_allocation"]["utilities_scaled"][0])

    def test_decorated_cycles_match_independent_edge_dfs(self):
        report = cores.audit(multicores_instance())
        actual = {tuple((edge["source"], edge["target"], edge["core_id"]) for edge in cycle["edges"])
                  for cycle in report["decorated_cycles"]}
        self.assertEqual(len(actual), report["summary"]["decorated_cycle_count"])
        self.assertEqual(actual, independent_cycle_oracle(report["champion_records"]))

    def test_disjoint_two_cycle_with_one_charity_core_is_verified(self):
        instance = multicores_instance()
        edges = [{"source": 0, "target": 1, "goods": [2, 5]},
                 {"source": 1, "target": 0, "goods": [0, 1]}]
        exchange = cores.construct_cycle_exchange(instance, edges)
        self.assertEqual(exchange["base_owner"], [1, 1, 0, 2, 3, 0])
        self.assertEqual(exchange["utility_gains_scaled"], [1, 1, 0, 0])
        self.assertEqual(exchange["charity"], [])
        self.assertTrue(exchange["is_efx"])
        self.assertTrue(exchange["fixed_order_lexicographic_improvement"])

    def test_zero_charity_cycle_is_legal(self):
        values = [[1, 2, 1, 1, 1], [2, 1, 1, 1, 1], [1] * 5, [1] * 5]
        instance = cores.parse_instance(document(values, [0, 1, 2, 3, None]))
        exchange = cores.construct_cycle_exchange(instance,
                    [{"source": 0, "target": 1, "goods": [1]},
                     {"source": 1, "target": 0, "goods": [0]}])
        self.assertEqual(exchange["base_owner"], [1, 0, 2, 3, None])
        self.assertEqual(exchange["charity"], [4])
        self.assertTrue(exchange["is_efx"])
        self.assertTrue(exchange["is_pareto_improvement"])

    def test_unused_physical_goods_all_return_to_charity(self):
        values = [[4, 1, 1, 1, 1, 1, 3]] + [[1, 1, 1, 2, 2, 2, 1] for _ in range(3)]
        instance = cores.parse_instance(document(values, [0, 0, 0, 1, 2, 3, None]))
        exchange = cores.construct_cycle_exchange(instance, [{"source": 0, "target": 0, "goods": [0, 6]}])
        self.assertEqual(exchange["base_owner"], [0, None, None, 1, 2, 3, 0])
        self.assertEqual(exchange["charity"], [1, 2])
        self.assertEqual(exchange["utility_gains_scaled"], [1, 0, 0, 0])
        self.assertTrue(exchange["is_efx"])
        self.assertTrue(exchange["is_pareto_improvement"])

    def test_exact_rationals_no_binary_float_and_weak_deletion_ties(self):
        instance = cores.parse_instance(document([["1/3"] * 5 for _ in range(4)], [0, 1, 2, 3, None]))
        report = cores.audit(instance)
        self.assertEqual(report["arithmetic"]["common_denominator"], 3)
        self.assertEqual(report["summary"], cores.audit(uniform_instance())["summary"])
        self.assertTrue(all(item["slacks_scaled"] == [0, 0, 0, 0]
                            for core in report["cores"] for item in core["single_deletion_slacks_scaled"]))
        actual = {(item["target"], tuple(item["goods"]), tuple(item["champions"])) for item in report["cores"]}
        self.assertEqual(actual, independent_core_oracle(instance))

    def test_calibration_all_cores_and_unique_three_cycle(self):
        instance = cores.load_instance(ARCHIVE, archive=True)
        report = cores.audit(instance)
        self.assertEqual(report["summary"], {
            "nonempty_core_subsets_checked_by_target": [7, 15, 7, 3],
            "core_count": 4, "core_count_by_target": [1, 1, 1, 1],
            "champion_record_count": 6, "simple_vertex_cycles_examined": 24,
            "decorated_cycle_count": 1, "decorated_self_loop_count": 0,
            "decorated_cycle_count_by_length": {"1": 0, "2": 0, "3": 1, "4": 0},
            "disjoint_core_cycle_count": 0, "minimum_charity_occurrences_on_cycle": 2})
        actual = {(item["target"], tuple(item["goods"]), tuple(item["champions"])) for item in report["cores"]}
        self.assertEqual(actual, {(0, (6, 8), (1, 2, 3)), (1, (2, 3, 8), (2,)),
                                  (2, (4, 8), (3,)), (3, (5,), (1,))})
        self.assertEqual(actual, independent_core_oracle(instance))
        cycle, = report["decorated_cycles"]
        self.assertEqual(cycle["vertices"], [1, 3, 2])
        self.assertEqual([(edge["source"], edge["target"], edge["goods"]) for edge in cycle["edges"]],
                         [(1, 3, [5]), (3, 2, [4, 8]), (2, 1, [2, 3, 8])])
        self.assertEqual(cycle["charity_occurrences"], 2)
        self.assertIsNone(cycle["exchange"])
        self.assertFalse(report["scope"]["global_lexmax_verified"])
        self.assertFalse(report["scope"]["global_maximality_claims_from_archive_used"])
        self.assertFalse(report["scope"]["complete_efx_nonexistence_claimed"])
        self.assertFalse(report["scope"]["downstream_two_cycle_or_role_layout_proved"])

    def test_global_calibration_retained_residual_payments(self):
        # The earlier complete 5**9 audit supplies this fixture's global premise.
        # Here independently recheck only the physical Corollary 3a inequalities.
        instance = cores.load_instance(ARCHIVE, archive=True)
        report = cores.audit(instance)
        base = report["base_allocation"]
        p, = base["charity"]
        own = base["utilities_scaled"]
        rows = instance.values_scaled
        for core in report["cores"]:
            target = core["target"]
            original = set(base["bundles"][target])
            if p not in core["goods"]:
                self.assertEqual(set(core["goods"]), original)
                continue
            retained = set(core["goods"]) - {p}
            residual = original - retained
            self.assertTrue(retained)
            self.assertTrue(residual)
            self.assertEqual(retained | residual, original)
            self.assertNotIn(target, core["champions"])
            self.assertGreater(sum(rows[target][g] for g in residual), rows[target][p])
            for champion in core["champions"]:
                deficit = own[champion] - sum(rows[champion][g] for g in retained)
                self.assertGreater(deficit, 0)
                self.assertLess(deficit, rows[champion][p])
            for observer in range(4):
                self.assertLessEqual(sum(rows[observer][g] for g in retained), own[observer])
                for deleted in retained:
                    self.assertLessEqual(sum(rows[observer][g] for g in retained - {deleted})
                                         + rows[observer][p], own[observer])

    def test_archive_global_claims_are_not_imported_and_scaled_metadata_is_checked(self):
        archive = json.loads(ARCHIVE.read_text())
        original = cores.audit(cores.parse_instance(archive, archive=True))
        archive["candidate"]["attains_domain_maximum"] = {"all_partial_efx": False}
        archive["domains"] = {"untrusted_global_claim": "not read"}
        self.assertEqual(cores.audit(cores.parse_instance(archive, archive=True)), original)
        archive["candidate"]["utilities_scaled"][0] += 1
        with self.assertRaisesRegex(ValueError, "utilities_scaled"):
            cores.parse_instance(archive, archive=True)

    def test_forged_core_and_malformed_cycle_records_rejected(self):
        instance = multicores_instance()
        malformed = [[], [{"source": 0, "target": 0, "goods": [0, 1]}],
                     [{"source": 1, "target": 0, "goods": [0, 1, 5]}],
                     [{"source": 0, "target": 1, "goods": [2, 2, 5]}],
                     [{"source": 0, "target": 1, "goods": [2, 4, 5]}],
                     [{"source": False, "target": 1, "goods": [2, 5]}],
                     [{"source": 0, "target": 1, "goods": [2, 5]}],
                     [{"source": 0, "target": 1, "goods": [2, 5]},
                      {"source": 0, "target": 1, "goods": [2, 5]}]]
        for edges in malformed:
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                cores.construct_cycle_exchange(instance, edges)

    def test_nonphysical_nonsafe_nonefx_inputs_rejected(self):
        original = document([[1] * 5 for _ in range(4)], [0, 1, 2, 3, None])
        for owners in ([0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3, True],
                       [0, 1, 2, 3, -1], [0, 1, 2, 3, 0], [0, 1, 2, None, None]):
            data = deepcopy(original)
            data["candidate"]["base_owner"] = owners
            with self.subTest(owners=owners), self.assertRaises(ValueError):
                cores.parse_instance(data)
        unsafe = deepcopy(original)
        unsafe["values"][0][4] = 2
        with self.assertRaisesRegex(ValueError, "not safe"):
            cores.parse_instance(unsafe)
        nonefx = document([[1, 1, 1, 1, 1, 1], [4, 4, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]], [0, 0, 1, 2, 3, None])
        with self.assertRaisesRegex(ValueError, "not EFX"):
            cores.parse_instance(nonefx)
        for field, declaration in (("bundles", [[0, 0], [1], [2], [3]]), ("charity", [4, 4]),
                                   ("is_efx", False), ("utilities_scaled", [2, 1, 1, 1])):
            data = deepcopy(original)
            data["candidate"][field] = declaration
            with self.subTest(field=field), self.assertRaises(ValueError):
                cores.parse_instance(data)

    def test_nonpositive_nonnumeric_and_bad_schema_rejected(self):
        original = document([[1] * 5 for _ in range(4)], [0, 1, 2, 3, None])
        for value in (0, -1, "0/3", "nan", "1/0", True, 0.1, {}, []):
            data = deepcopy(original)
            data["values"][0][0] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                cores.parse_instance(data)
        for field, value in (("schema", "unsupported"), ("n", 3), ("n", True),
                             ("m", 4), ("m", True), ("agent_order", [False, 1, 2, 3])):
            data = deepcopy(original)
            data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                cores.parse_instance(data)
        with self.assertRaises(ValueError):
            cores.load_instance(ARCHIVE)

    def test_json_decimals_exact_and_duplicates_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            data = document([[0.1] * 5 for _ in range(4)], [0, 1, 2, 3, None])
            source.write_text(json.dumps(data))
            instance = cores.load_instance(source)
            self.assertEqual(instance.denominator, 10)
            self.assertEqual(instance.values_scaled, ((1, 1, 1, 1, 1),) * 4)
            for text in ('{"schema":"a","schema":"b"}', '{"value": NaN}', '{"value": Infinity}'):
                source.write_text(text)
                with self.assertRaises(ValueError):
                    cores.load_instance(source)

    def test_enumeration_bounds_and_incomplete_core_scan_fail_closed(self):
        data = document([[1] * 5 for _ in range(4)], [0, 1, 2, 3, None])
        with self.assertRaises(ValueError):
            cores.parse_instance(data, max_goods=4)
        with self.assertRaisesRegex(ValueError, "decorated cycles exceed"):
            cores.audit(uniform_instance(), max_decorated_cycles=1)
        with patch.object(cores, "combinations", return_value=iter(())):
            with self.assertRaisesRegex(RuntimeError, "incomplete core-subset"):
                cores.extract_cores(uniform_instance())

    def test_cli_stdout_is_deterministic_and_error_has_no_partial_report(self):
        outputs = []
        for _ in range(2):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(cores.main([str(ARCHIVE), "--archive"]), 0)
            outputs.append(output.getvalue())
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(json.loads(outputs[0])["schema"], cores.OUTPUT_SCHEMA)
        output, error = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(error):
            self.assertEqual(cores.main([str(ARCHIVE), "--archive", "--max-goods", "8"]), 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("max_goods", error.getvalue())


if __name__ == "__main__":
    unittest.main()
