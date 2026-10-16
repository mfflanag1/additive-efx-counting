"""Physical-state identities and rejection controls; no admission claim."""

from contextlib import redirect_stdout
from fractions import Fraction
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tracks/physical_admission/verify_state_separation.py"
SPEC = importlib.util.spec_from_file_location("physical_state_separation", SCRIPT)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)
ARCHIVE = ROOT / "docs/global-admission/references/a1_source/fixed_u_twelve_atom_four_edge_residuals_20260826.json"


class PhysicalStateTests(unittest.TestCase):
    def test_literal_base_and_wall_calibration(self):
        report = verifier.verify_profile(verifier.base_calibration(), require_root_wall=True)
        self.assertTrue(report["valid"])
        self.assertEqual(report["physical_good_count"], 12)
        self.assertEqual(report["base_pool_cardinality"], 3)
        self.assertEqual(report["support_pool_cardinality"], 1)
        self.assertTrue(report["base_outside_at_most_one_pool_class"])
        self.assertFalse(report["support_physical_efx"])
        self.assertFalse(report["boundary"]["universal_A1_admission_proved"])
        self.assertFalse(report["boundary"]["global_selector_or_reachability_verified"])

    def test_all_48_role_bounds_have_exact_certificates(self):
        report = verifier.verify_profile(verifier.base_calibration())
        certificates = report["role_upper_bound_certificates"]
        self.assertEqual(len(certificates), 48)
        self.assertEqual({c["method"] for c in certificates},
                         {"own_proper_subset", "safe_pool_proper_subset", "foreign_physical_deletion"})
        for certificate in certificates:
            self.assertLessEqual(Fraction(certificate["value"]), Fraction(certificate["dominating_value"]))
            self.assertLessEqual(Fraction(certificate["dominating_value"]), 1)
            self.assertTrue(certificate["strict_for_this_profile"])

    def test_wall_names_an_actual_failed_physical_deletion(self):
        data = verifier.base_calibration()
        roles, values = verifier.parse_profile(data)
        state = verifier.expand(verifier.SUPPORT, roles)
        report = verifier.verify_profile(data, require_root_wall=True)
        violation = report["root_wall"]["specific_efx_violation"]
        self.assertIn(violation, verifier.efx_violations(values, state))
        self.assertGreater(Fraction(violation["residual"]), Fraction(violation["own"]))

    def test_signed_transfer_includes_charity_in_both_directions(self):
        data = verifier.base_calibration()
        ledger = verifier.verify_profile(data)["signed_transfers"]
        self.assertEqual(len(ledger["moves"]), 8)
        self.assertEqual({m["role"] for m in ledger["moves"] if m["from"] == "pool"}, {"j", "l", "gr"})
        self.assertEqual({m["role"] for m in ledger["moves"] if m["to"] == "pool"}, {"p"})
        for owner in verifier.OWNERS:
            delta = ledger["delta_by_observer_and_holder"][owner]
            row = {g: Fraction(v) for g, v in data["values"][owner].items()}
            self.assertEqual(Fraction(delta["pool"]), row["p"] - row["j"] - row["l"] - row["gr"])
            self.assertEqual(sum(map(Fraction, delta.values())), 0)

    def test_missing_role_rejected(self):
        data = verifier.base_calibration()
        del data["roles"]["gr"]
        with self.assertRaisesRegex(verifier.ValidationError, "twelve literal roles"):
            verifier.verify_profile(data)

    def test_empty_role_rejected(self):
        data = verifier.base_calibration()
        data["roles"]["gr"] = []
        with self.assertRaisesRegex(verifier.ValidationError, "nonempty physical packet"):
            verifier.verify_profile(data)

    def test_overlapping_or_repeated_role_good_rejected(self):
        for packet in (["j"], ["gr", "gr"]):
            data = verifier.base_calibration()
            data["roles"]["gr"] = packet
            with self.assertRaisesRegex(verifier.ValidationError, "overlap or repeat"):
                verifier.verify_profile(data)

    def test_missing_or_extra_physical_value_rejected(self):
        for extra in (False, True):
            data = verifier.base_calibration()
            if extra:
                data["values"]["r"]["ghost"] = "1"
            else:
                del data["values"]["r"]["j"]
            with self.assertRaisesRegex(verifier.ValidationError, "exactly the physical goods"):
                verifier.verify_profile(data)

    def test_inexact_nonpositive_values_rejected(self):
        for invalid in (0, -1, 0.1, True, "0", "1/0"):
            data = verifier.base_calibration()
            data["values"]["r"]["j"] = invalid
            with self.assertRaises(verifier.ValidationError):
                verifier.verify_profile(data)

    def test_own_normalization_is_not_assumed(self):
        data = verifier.base_calibration()
        data["values"]["r"]["a0"] = "1"
        with self.assertRaisesRegex(verifier.ValidationError, "not normalized"):
            verifier.verify_profile(data)

    def test_unsafe_pool_is_not_assumed_away(self):
        data = verifier.base_calibration()
        data["values"]["r"]["j"] = "2"
        with self.assertRaisesRegex(verifier.ValidationError, "pool is unsafe"):
            verifier.verify_profile(data)

    def test_coarse_role_tail_can_miss_physical_efx_violation(self):
        roles = {role: [role] for role in verifier.ROLES}
        roles["a0"] = ["a0i", "a0ii"]
        base = verifier.expand(verifier.BASE, roles)
        goods = [g for role in verifier.ROLES for g in roles[role]]
        values = {owner: {g: str(Fraction(1, len(base[owner])) if g in base[owner] else Fraction(1, 20))
                          for g in goods} for owner in verifier.OWNERS}
        values["q"].update(a0i="2/5", a0ii="2/5", m="7/10")
        data = {"schema": verifier.SCHEMA, "roles": roles, "values": values}
        self.assertEqual(verifier.tail({"a0": Fraction(4, 5), "m": Fraction(7, 10)}, ("a0", "m")), Fraction(4, 5))
        self.assertEqual(verifier.tail({g: Fraction(v) for g, v in values["q"].items()}, base["r"]), Fraction(11, 10))
        with self.assertRaisesRegex(verifier.ValidationError, "base is not physical EFX"):
            verifier.verify_profile(data)

    def test_multigood_role_preserves_total_but_changes_support_pool_size(self):
        data = verifier.base_calibration()
        data["roles"]["p"] = ["p0", "p1"]
        for owner in verifier.OWNERS:
            amount = Fraction(data["values"][owner].pop("p"))
            data["values"][owner].update(p0=str(amount / 2), p1=str(amount / 2))
        report = verifier.verify_profile(data, require_root_wall=True)
        self.assertEqual(report["physical_good_count"], 13)
        self.assertEqual(report["support_pool_cardinality"], 2)
        self.assertEqual(len(report["role_upper_bound_certificates"]), 48)

    def test_wall_failure_not_implied_by_base_constraints(self):
        data = verifier.base_calibration()
        for role in ("a0", "a1"):
            data["values"]["d"][role] = "1/10000"
        self.assertFalse(verifier.verify_profile(data)["root_wall"]["holds"])
        with self.assertRaisesRegex(verifier.ValidationError, "root-facing wall does not hold"):
            verifier.verify_profile(data, require_root_wall=True)

    def test_global_singleton_calibration_has_complete_efx(self):
        report = verifier.singleton_calibration()
        self.assertEqual(report["all_partial_allocations_checked"], 625)
        self.assertEqual(report["partial_efx_count"], 209)
        self.assertEqual(report["unique_global_lex_maximum"], [0, 1, 2, 3])
        self.assertEqual(report["normalized_cross_singleton_value"], "27")
        self.assertTrue(report["winner_is_complete_efx"])
        self.assertTrue(report["not_a_no_complete_efx_or_global_admission_counterexample"])

    def test_archived_profiles_replay_only_declared_constraints(self):
        report = verifier.verify_archive(ARCHIVE)
        self.assertEqual(set(report["records"]), {"g4_b3", "g4_b5"})
        for profile in report["records"].values():
            self.assertTrue(profile["valid"])
            self.assertTrue(profile["root_wall"]["holds"])
            self.assertFalse(profile["support_physical_efx"])
        self.assertIn("does not replay other master premises", report["boundary"])

    def test_archive_wrong_record_set_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{}")
            with self.assertRaisesRegex(verifier.ValidationError, "two declared"):
                verifier.verify_archive(path)

    def test_serialized_duplicate_schema_roles_and_values_rejected(self):
        encoded = json.dumps(verifier.base_calibration())
        variants = {
            "schema": encoded.replace('"schema":', '"schema": "hidden-invalid-schema", "schema":', 1),
            "role": encoded.replace('"roles": {', '"roles": {"a0": ["hidden-overlap"], ', 1),
            "value": encoded.replace('"values": {"r": {', '"values": {"r": {"a0": "-1", ', 1),
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            for label, document in variants.items():
                with self.subTest(label=label):
                    # Ordinary JSON would hide the bad first value behind the valid second.
                    self.assertEqual(json.loads(document), verifier.base_calibration())
                    path.write_text(document)
                    with self.assertRaisesRegex(verifier.ValidationError, "duplicate JSON key"):
                        verifier.main(["--profile", str(path)])

    def test_archive_duplicate_record_and_valuation_keys_rejected(self):
        encoded = ARCHIVE.read_text()
        variants = [encoded.replace('"g4_b3": {', '"g4_b3": {}, "g4_b3": {', 1),
                    encoded.replace('"valuation": {', '"valuation": {"a0:r": "-1", ', 1)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate-archive.json"
            for document in variants:
                self.assertEqual(json.loads(document), json.loads(encoded))
                path.write_text(document)
                with self.assertRaisesRegex(verifier.ValidationError, "duplicate JSON key"):
                    verifier.main(["--archive", str(path)])

    def test_json_nonfinite_and_decimal_numbers_rejected_in_both_entry_points(self):
        for flag, encoded in (("--profile", json.dumps(verifier.base_calibration())),
                              ("--archive", ARCHIVE.read_text())):
            for token in ("NaN", "Infinity", "-Infinity", "0.5", "1e999"):
                with self.subTest(flag=flag, token=token), tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "number.json"
                    # Rejection is global, including otherwise ignored metadata.
                    path.write_text('{"invalid_metadata": ' + token + ',' + encoded[1:])
                    with self.assertRaisesRegex(verifier.ValidationError, "JSON numbers must be integers"):
                        verifier.main([flag, str(path)])

    def test_exact_json_accepts_integer_and_rational_string_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "exact.json"
            path.write_text('{"integer": 2, "rational": "1/3", "exact_decimal_string": "0.5"}')
            self.assertEqual(verifier.read_exact_json(path),
                             {"integer": 2, "rational": "1/3", "exact_decimal_string": "0.5"})

    def test_cli_default_output_is_deterministic_and_scoped(self):
        outputs = []
        for _ in range(2):
            stream = io.StringIO()
            with redirect_stdout(stream):
                verifier.main(["--require-root-wall"])
            outputs.append(stream.getvalue())
        self.assertEqual(*outputs)
        report = json.loads(outputs[0])
        self.assertFalse(report["boundary"]["universal_A1_admission_proved"])


if __name__ == "__main__":
    unittest.main()
