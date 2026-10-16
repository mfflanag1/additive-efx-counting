"""Tiny exhaustive checks for the standalone exact selector audit."""

from fractions import Fraction
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "tracks/selector_compatibility/independent_enumerator.py"
SPEC = importlib.util.spec_from_file_location("independent_selector_enumerator", SCRIPT)
enumerator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = enumerator
SPEC.loader.exec_module(enumerator)


def document(values, owners):
    return {
        "schema": enumerator.INPUT_SCHEMA, "n": 4, "m": len(values[0]),
        "agent_order": [0, 1, 2, 3], "values": values,
        "candidate": {"base_owner": owners},
    }


def instance(values, owners):
    return enumerator.parse_instance(document(values, owners))


class ExactEnumeratorTests(unittest.TestCase):
    def test_single_good_complete_included_and_candidate_not_assumed_maximal(self):
        report = enumerator.audit(instance([[1]] * 4, [None]))
        self.assertEqual(report["enumeration"]["visited_assignment_count"], 5)
        self.assertEqual(report["domains"]["all_partial_efx"]["allocation_count"], 5)
        for name in ("all_partial_efx_safe", "at_most_one_charity_efx_safe", "complete_efx"):
            self.assertEqual(report["domains"][name]["allocation_count"], 4)
            self.assertEqual(report["domains"][name]["maximum_utility_key"], [1, 0, 0, 0])
            self.assertEqual(report["domains"][name]["maximizer"]["base_owner"], [0])
        self.assertEqual(report["domains"]["exactly_one_charity_efx_safe"]["allocation_count"], 0)
        self.assertIsNone(report["domains"]["exactly_one_charity_efx_safe"]["maximizer"])
        self.assertFalse(report["candidate"]["attains_domain_maximum"]["all_partial_efx"])

    def test_physical_conservation_and_duplicate_bundles_rejected(self):
        data = document([[1, 1]] * 4, [0, None])
        data["candidate"]["bundles"] = [[0, 0], [], [], []]
        with self.assertRaisesRegex(ValueError, "duplicate or missing"):
            enumerator.parse_instance(data)
        for owners in ([0], [0, 4], [0, True], [0, 0, None], [0, -1]):
            with self.subTest(owners=owners), self.assertRaises(ValueError):
                enumerator.parse_instance(document([[1, 1]] * 4, owners))
        valid = instance([[1, 1]] * 4, [0, None])
        with self.assertRaises(ValueError):
            enumerator.allocation_record(valid, [0, 4])

    def test_every_deleted_good_checked_not_only_most_valuable(self):
        values = [[5, 10, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]
        record = enumerator.allocation_record(instance(values, [0, 1, 1]), [0, 1, 1])
        comparisons = {(c["observer"], c["target"], c["deleted_good"]): c for c in record["efx_comparisons"]}
        self.assertEqual(comparisons[0, 1, 1]["slack_scaled"], 4)
        self.assertEqual(comparisons[0, 1, 2]["slack_scaled"], -5)
        self.assertFalse(record["is_efx"])
        self.assertEqual(len(record["efx_comparisons"]), 12)

    def test_whole_charity_pool_not_individual_goods(self):
        values = [[3, 3, 3, 3, 2, 2]] * 4
        owners = [0, 1, 2, 3, None, None]
        record = enumerator.allocation_record(instance(values, owners), owners)
        self.assertTrue(record["is_efx"])
        self.assertFalse(record["whole_charity_nonenvy"])
        self.assertEqual(record["charity_nonenvy_slacks_scaled"], [-1] * 4)

    def test_exact_rationals_and_ties_are_retained(self):
        report = enumerator.audit(instance([["1/3", "1/3"]] * 4, [0, 1]))
        self.assertEqual(report["arithmetic"]["common_denominator"], 3)
        result = report["domains"]["complete_efx"]
        self.assertEqual(result["allocation_count"], 12)
        self.assertEqual(result["maximum_utility_key"], ["1/3", "1/3", 0, 0])
        self.assertEqual(result["maximum_utility_key_scaled"], [1, 1, 0, 0])
        self.assertEqual(result["maximizer_count"], 2)
        self.assertEqual(result["maximizer"]["base_owner"], [0, 1])

    def test_exhaustive_counts_match_direct_fraction_deletion_oracle(self):
        values = [[Fraction((i + 1) * (g + 2) % 7 + 1, g + 1) for g in range(4)] for i in range(4)]
        report = enumerator.audit(instance(values, [0, 1, 2, 3]))
        expected = {name: [] for name in enumerator.DOMAIN_DEFINITIONS}
        for owners in product((0, 1, 2, 3, None), repeat=4):
            bundles = [[g for g in range(4) if owners[g] == i] for i in range(4)]
            pool = [g for g in range(4) if owners[g] is None]
            utility = tuple(sum((values[i][g] for g in bundles[i]), Fraction(0)) for i in range(4))
            efx = all(utility[i] >= sum((values[i][g] for g in bundles[j] if g != deleted), Fraction(0))
                      for i in range(4) for j in range(4) for deleted in bundles[j])
            safe = all(utility[i] >= sum((values[i][g] for g in pool), Fraction(0)) for i in range(4))
            flags = (efx, efx and safe, efx and safe and len(pool) <= 1,
                     efx and safe and len(pool) == 1, efx and not pool)
            for name, flag in zip(expected, flags):
                if flag:
                    expected[name].append(utility)
        for name, utilities in expected.items():
            with self.subTest(domain=name):
                actual = report["domains"][name]
                self.assertEqual(actual["allocation_count"], len(utilities))
                if utilities:
                    self.assertEqual(tuple(map(Fraction, actual["maximum_utility_key"])), max(utilities))
                    self.assertEqual(actual["maximizer_count"], utilities.count(max(utilities)))

    def test_improving_out_of_class_assignment_reported_when_it_exists(self):
        report = enumerator.audit(instance([[1, 1, 1]] * 4, [None, None, None]))
        witness = report["globally_improving_out_of_class_efx_assignment"]
        self.assertIsNotNone(witness)
        self.assertTrue(witness["is_efx"])
        self.assertFalse(witness["domain_membership"]["at_most_one_charity_efx_safe"])
        self.assertGreater(tuple(witness["utilities_scaled"]), (0, 0, 0, 0))

    def test_malformed_nonpositive_nonrational_and_unsupported_inputs_fail(self):
        for bad in (0, -1, "0/3", "nan", "1/0", True, 0.1, {}, []):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                enumerator.parse_instance(document([[bad]] * 4, [0]))
        for field, value in (("schema", "unknown"), ("n", True), ("n", 3), ("m", True),
                             ("agent_order", [1, 0, 2, 3]), ("agent_order", [False, 1, 2, 3])):
            data = document([[1]] * 4, [0])
            data[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                enumerator.parse_instance(data)
        with self.assertRaises(ValueError):
            enumerator.parse_instance(document([[1, 1]] * 4, [0, 1]), max_goods=1)

    def test_json_decimal_exact_duplicate_and_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            data = document([[1]] * 4, [0])
            source.write_text(json.dumps(data).replace("[[1], [1], [1], [1]]", "[[0.1], [0.1], [0.1], [0.1]]"))
            self.assertEqual(enumerator.load_instance(source).values[0][0], Fraction(1, 10))
            for text in ('{"schema":"a","schema":"b"}', '{"value": NaN}', '{"value": Infinity}'):
                source.write_text(text)
                with self.assertRaises(ValueError):
                    enumerator.load_instance(source)

    def test_incomplete_enumeration_fails_closed(self):
        with patch.object(enumerator, "product", return_value=iter([(0,)])):
            with self.assertRaisesRegex(RuntimeError, "incomplete enumeration"):
                enumerator.audit(instance([[1]] * 4, [0]))

    def test_output_deterministic_and_cli_bound(self):
        data = document([[1, 2]] * 4, [0, 1])
        self.assertEqual(enumerator.audit(enumerator.parse_instance(data)), enumerator.audit(enumerator.parse_instance(data)))
        with tempfile.TemporaryDirectory() as directory:
            source, target = Path(directory) / "input.json", Path(directory) / "output.json"
            source.write_text(json.dumps(data))
            self.assertEqual(enumerator.main([str(source), "--output", str(target)]), 0)
            first = target.read_bytes()
            self.assertEqual(enumerator.main([str(source), "--output", str(target)]), 0)
            self.assertEqual(target.read_bytes(), first)
            self.assertEqual(enumerator.main([str(source), "--max-goods", "1", "--output", str(target)]), 2)
            self.assertEqual(target.read_bytes(), first)


if __name__ == "__main__":
    unittest.main()
