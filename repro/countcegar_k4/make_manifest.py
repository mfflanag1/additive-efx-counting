#!/usr/bin/env python3
"""Create the manifest only after the terminal checks and regression passes."""

import hashlib
import json
import lzma
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pysat
import z3
from ortools import __version__ as ortools_version
from ortools.sat.python import cp_model, cp_model_helper
from pysat.formula import CNF

import check_sat
from check_z3 import build_pb_cardinality_master
from reconstruct import build_master
from verify import (
    check_allocation,
    enumerate_all,
    masks_from_assign,
    precompute,
)


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def relative(path):
    return str(Path(path).resolve().relative_to(ROOT))


def file_record(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": relative(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def compressed_record(path):
    digest = hashlib.sha256()
    size = 0
    with lzma.open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
            size += len(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def load_json(path):
    return json.loads(Path(path).read_text())


def canonical_pool_hash(pool):
    payload = json.dumps(pool, separators=(",", ":")) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


def deduplicate(pool):
    unique = []
    seen = set()
    for assign in pool:
        key = tuple(assign)
        if key not in seen:
            seen.add(key)
            unique.append(assign)
    return unique


def replay_trace(historical_pool, complete_pool, trace_path):
    pool = deduplicate(historical_pool)
    known = {tuple(assign) for assign in pool}
    records = [
        json.loads(line)
        for line in trace_path.read_text().splitlines()
        if line.strip()
    ]
    for expected_round, record in enumerate(records, start=1):
        if record.get("round") != expected_round:
            raise ValueError("non-sequential reconstruction trace round")
        values = record["values"]
        if (
            len(values) != 4
            or any(len(row) != 7 for row in values)
            or any(
                type(value) is not int or not 1 <= value <= 4
                for row in values
                for value in row
            )
        ):
            raise ValueError(f"invalid valuation in trace round {expected_round}")
        if any(values[i] < values[i + 1] for i in range(3)):
            raise ValueError(f"row lex violation in trace round {expected_round}")
        columns = [[values[i][g] for i in range(4)] for g in range(7)]
        if any(columns[g] < columns[g + 1] for g in range(6)):
            raise ValueError(
                f"column lex violation in trace round {expected_round}"
            )
        val, minall, minpos = precompute(4, 7, values)
        pooled_survivors = sum(
            check_allocation(
                4,
                masks_from_assign(4, assign),
                val,
                minall,
                minpos,
            )[0]
            for assign in pool
        )
        if pooled_survivors > 3:
            raise ValueError(
                f"candidate violates master in trace round {expected_round}"
            )
        checked = enumerate_all(4, 7, values, collect=16)
        if checked["efx0_count"] != record.get("efx0_count"):
            raise ValueError(
                f"EFX0 count mismatch in trace round {expected_round}"
            )
        additions = []
        for assign in checked["examples_efx0"]:
            key = tuple(assign)
            if key not in known:
                known.add(key)
                additions.append(assign)
        if additions != record.get("added"):
            raise ValueError(
                f"added cuts mismatch in trace round {expected_round}"
            )
        pool.extend(additions)
        if len(pool) != record.get("pool_size"):
            raise ValueError(
                f"pool size mismatch in trace round {expected_round}"
            )
        if canonical_pool_hash(pool) != record.get("pool_sha256"):
            raise ValueError(
                f"pool hash mismatch in trace round {expected_round}"
            )
    if pool != complete_pool:
        raise ValueError("trace replay does not reproduce terminal pool")
    return {
        "status": "PASS",
        "initial_unique_pool_size": len(deduplicate(historical_pool)),
        "sat_rounds": len(records),
        "terminal_pool_size": len(pool),
    }


def run():
    historical_pool_path = ROOT / "results/countpool_K4.json"
    complete_pool_path = ROOT / "results/countpool_K4_complete.json"
    reconstructed_result_path = (
        ROOT / "results/countcegar_K4_reconstructed.json"
    )
    reconstruction_run_path = (
        ROOT / "results/countcegar_K4_reconstruction_run.json"
    )
    z3_result_path = ROOT / "results/countcegar_K4_z3.json"
    boundary_path = ROOT / "results/countcegar_slot_boundary.json"
    smt2_path = ROOT / "results/countcegar_K4_complete.smt2"
    cp_model_path = ROOT / "results/countcegar_K4_complete_model.pbtxt"
    cp_response_path = (
        ROOT / "results/countcegar_K4_complete_response.pbtxt"
    )
    cp_stats_path = ROOT / "results/countcegar_K4_complete_stats.txt"
    sat_cnf_path = ROOT / "results/countcegar_K4_sat.cnf"
    sat_result_path = ROOT / "results/countcegar_K4_sat.json"
    sat_replay_path = ROOT / "results/countcegar_K4_sat_replay.json"
    sat_differential_path = (
        ROOT / "results/countcegar_K4_sat_differential.json"
    )
    certificate_metadata_path = (
        HERE / "certificates/DRAT_CERTIFICATE.json"
    )

    historical_pool = load_json(historical_pool_path)
    complete_pool = load_json(complete_pool_path)
    reconstructed = load_json(reconstructed_result_path)
    reconstruction_run = load_json(reconstruction_run_path)
    independent = load_json(z3_result_path)
    direct_sat = load_json(sat_result_path)
    sat_replay = load_json(sat_replay_path)
    sat_differential = load_json(sat_differential_path)
    certificate = load_json(certificate_metadata_path)
    boundary = load_json(boundary_path)
    if deduplicate(complete_pool) != complete_pool:
        raise ValueError("terminal pool is not an ordered set of allocations")
    trace_replay = replay_trace(
        historical_pool,
        complete_pool,
        ROOT / "results/countcegar_K4_reconstruction.jsonl",
    )
    if (
        trace_replay["sat_rounds"] + 1
        != reconstruction_run.get("rounds_this_invocation")
    ):
        raise ValueError("trace length does not match the terminal round record")
    if reconstructed.get("status") != "UNSAT":
        raise ValueError("reconstructed CP-SAT result is not terminal UNSAT")
    if reconstruction_run.get("status") != "UNSAT":
        raise ValueError("fresh reconstruction run is not terminal UNSAT")
    if reconstruction_run.get("pool_sha256") != sha256(complete_pool_path):
        raise ValueError("fresh reconstruction result/pool hash mismatch")
    if independent.get("status") == "UNSAT":
        z3_role = "corroborating terminal verdict"
    elif (
        independent.get("status") == "UNKNOWN"
        and independent.get("reason_unknown") == "timeout"
    ):
        z3_role = "auxiliary timed-out check; not evidence for the claim"
    else:
        raise ValueError(
            "independent Z3 result is neither UNSAT nor timeout-UNKNOWN"
        )
    if direct_sat.get("status") != "UNSAT":
        raise ValueError("independent direct-SAT result is not terminal UNSAT")
    if sat_replay.get("status") != "UNSAT":
        raise ValueError("cold DIMACS replay is not terminal UNSAT")
    if sat_differential.get("status") != "PASS":
        raise ValueError("direct-SAT differential regression did not pass")
    if boundary.get("status") != "PASS":
        raise ValueError("slot boundary regression did not pass")
    direct_solver = direct_sat.get("solver", {})
    replay_solver = sat_replay.get("solver", {})
    if reconstructed.get("pool_sha256") != sha256(complete_pool_path):
        raise ValueError("reconstructed result/pool hash mismatch")
    if independent.get("pool_sha256") != sha256(complete_pool_path):
        raise ValueError("independent result/pool hash mismatch")
    if independent.get("smt2_sha256") != sha256(smt2_path):
        raise ValueError("independent result/SMT-LIB2 hash mismatch")
    if direct_sat.get("pool_sha256") != sha256(complete_pool_path):
        raise ValueError("direct-SAT result/pool hash mismatch")
    if direct_sat.get("deduplicated_pool_sha256") != canonical_pool_hash(
        complete_pool
    ):
        raise ValueError("direct-SAT result/deduplicated pool hash mismatch")
    if direct_sat.get("dimacs_sha256") != sha256(sat_cnf_path):
        raise ValueError("direct-SAT result/DIMACS hash mismatch")
    if (
        certificate.get("schema") != 1
        or certificate.get("status") != "VERIFIED"
        or certificate.get("input", {}).get("path")
        != relative(sat_cnf_path)
        or certificate["input"].get("bytes") != sat_cnf_path.stat().st_size
        or certificate["input"].get("sha256") != sha256(sat_cnf_path)
        or certificate["input"].get("variables")
        != direct_sat.get("variables")
        or certificate["input"].get("clauses") != direct_sat.get("clauses")
    ):
        raise ValueError("DRAT certificate input metadata mismatch")
    proof_path = ROOT / certificate["proof"]["path"]
    proof_record = file_record(proof_path)
    if (
        certificate["proof"].get("format") != "binary DRAT"
        or certificate["proof"].get("compression") != "xz"
        or certificate["proof"].get("compressed_bytes")
        != proof_record["bytes"]
        or certificate["proof"].get("compressed_sha256")
        != proof_record["sha256"]
    ):
        raise ValueError("compressed DRAT proof metadata mismatch")
    uncompressed = compressed_record(proof_path)
    if (
        certificate["proof"].get("uncompressed_bytes")
        != uncompressed["bytes"]
        or certificate["proof"].get("uncompressed_sha256")
        != uncompressed["sha256"]
    ):
        raise ValueError("uncompressed DRAT proof metadata mismatch")
    generator = certificate.get("generator", {})
    certificate_checker = certificate.get("checker", {})
    if (
        generator.get("name") != "CaDiCaL"
        or generator.get("version") != "1.9.5"
        or generator.get("tag") != "rel-1.9.5"
        or generator.get("commit")
        != "146207318796f094dcded87349a64f0c6927309e"
        or generator.get("exit_code") != 20
        or generator.get("status") != "UNSATISFIABLE"
        or {
            "restarts": generator.get("restarts"),
            "conflicts": generator.get("conflicts"),
            "decisions": generator.get("decisions"),
            "propagations": generator.get("propagations"),
        }
        != direct_solver.get("statistics")
        or certificate_checker.get("name") != "drat-trim"
        or certificate_checker.get("commit")
        != "2e3b2dc0ecf938addbd779d42877b6ed69d9a985"
        or certificate_checker.get("binary_input_flag") != "-i"
        or certificate_checker.get("exit_code") != 0
        or certificate_checker.get("status") != "VERIFIED"
        or certificate_checker.get("resolution_steps") != 28212699
        or certificate_checker.get("rat_lemmas_in_core") != 0
    ):
        raise ValueError("DRAT tool or checker metadata mismatch")
    certificate_logs = [
        ROOT / generator["log"]["path"],
        ROOT / certificate_checker["log"]["path"],
    ]
    for log_path, record in zip(
        certificate_logs,
        [generator["log"], certificate_checker["log"]],
    ):
        if file_record(log_path) != {
            "path": record["path"],
            "bytes": record["bytes"],
            "sha256": record["sha256"],
        }:
            raise ValueError(f"DRAT log metadata mismatch: {log_path}")
    if "s VERIFIED" not in certificate_logs[1].read_text():
        raise ValueError("archived drat-trim log lacks VERIFIED verdict")
    if sat_replay.get("dimacs_sha256") != sha256(sat_cnf_path):
        raise ValueError("cold replay/DIMACS hash mismatch")
    if direct_sat.get("raw_pool_size") != len(complete_pool):
        raise ValueError("direct-SAT raw pool size mismatch")
    if direct_sat.get("unique_pool_size") != len(
        set(map(tuple, complete_pool))
    ):
        raise ValueError("direct-SAT unique pool size mismatch")
    if (
        direct_solver.get("requested") != "cadical195"
        or direct_solver.get("backend") != "Cadical195"
        or direct_solver.get("timeout_seconds") != 10800
    ):
        raise ValueError("direct-SAT solver settings mismatch")
    if (
        replay_solver.get("requested") != "cadical195"
        or replay_solver.get("backend") != "Cadical195"
        or replay_solver.get("timeout_seconds") != 10800
        or replay_solver.get("statistics") != direct_solver.get("statistics")
    ):
        raise ValueError("cold DIMACS replay solver metadata mismatch")
    differential_cases = sat_differential.get("differential_cases", [])
    isolated_process = sat_differential.get("isolated_solver_process", {})
    differential_sources = sat_differential.get("source_sha256", {})
    expected_case_names = {
        (matrix, case)
        for matrix in ("all_ones", "staircase")
        for case in (
            "empty",
            "three_efx0",
            "four_efx0",
            "non_efx0_only",
            "three_efx0_plus_non_efx0",
        )
    }
    expected_status_names = {
        "definition",
        "cnf_slots",
        "lia_slots",
        "lia_cardinality",
        "pb_slots",
        "pb_cardinality",
    }
    if (
        sat_differential.get("strong_envy_identity_checks") != 3003
        or sat_differential.get("lexicographic_comparator_checks") != 256
        or len(differential_cases) != 10
        or {
            (case.get("matrix"), case.get("case"))
            for case in differential_cases
        }
        != expected_case_names
        or isolated_process.get("successful_backend") != "Cadical195"
        or isolated_process.get("crash_exit_code") != 17
        or isolated_process.get("timeout_reason") != "wall-clock timeout"
        or not (
            0
            <= isolated_process.get("crash_detected_within_seconds", 2)
            < 2
        )
        or not (
            0
            <= isolated_process.get("timeout_detected_within_seconds", 2)
            < 2
        )
        or differential_sources.get("check_sat")
        != sha256(HERE / "check_sat.py")
        or differential_sources.get("check_z3")
        != sha256(HERE / "check_z3.py")
        or differential_sources.get("differential_test")
        != sha256(HERE / "test_sat_differential.py")
        or any(
            set(case.get("statuses", {})) != expected_status_names
            or any(
                status != case.get("expected_sat")
                for status in case["statuses"].values()
            )
            for case in differential_cases
        )
    ):
        raise ValueError("direct-SAT differential metadata mismatch")
    terminal_model = cp_model.CpModel()
    terminal_model.Proto().parse_text_format(cp_model_path.read_text())
    rebuilt_model, _ = build_master(4, complete_pool)
    if str(rebuilt_model.Proto()) != cp_model_path.read_text():
        raise ValueError("source+pool rebuilt model differs from archived model")
    rebuilt_z3, _, _ = build_pb_cardinality_master(4, complete_pool)
    if rebuilt_z3.to_smt2() != smt2_path.read_text():
        raise ValueError("source+pool rebuilt SMT2 differs from archived SMT2")
    parsed_cnf = CNF(from_file=str(sat_cnf_path))
    rebuilt_cnf, _, _, rebuilt_vpool = check_sat.build_master(complete_pool)
    with tempfile.TemporaryDirectory() as directory:
        rebuilt_cnf_path = Path(directory) / "rebuilt.cnf"
        rebuilt_cnf.to_file(str(rebuilt_cnf_path))
        if rebuilt_cnf_path.read_bytes() != sat_cnf_path.read_bytes():
            raise ValueError("source+pool rebuilt DIMACS differs from archive")
    if (
        parsed_cnf.nv != direct_sat.get("variables")
        or len(parsed_cnf.clauses) != direct_sat.get("clauses")
        or rebuilt_cnf.nv != parsed_cnf.nv
        or len(rebuilt_cnf.clauses) != len(parsed_cnf.clauses)
        or rebuilt_vpool.top
        != direct_sat.get("named_and_auxiliary_variables")
        or sat_replay.get("variables") != parsed_cnf.nv
        or sat_replay.get("clauses") != len(parsed_cnf.clauses)
    ):
        raise ValueError("direct-SAT CNF metadata mismatch")
    terminal_response = cp_model_helper.CpSolverResponse()
    terminal_response.parse_text_format(cp_response_path.read_text())
    if terminal_response.status != cp_model.INFEASIBLE:
        raise ValueError("parsed CpSolverResponse is not INFEASIBLE")
    expected_export_hashes = {
        "cp_model_sha256": cp_model_path,
        "cp_solver_response_sha256": cp_response_path,
        "cp_solver_stats_sha256": cp_stats_path,
    }
    for field, path in expected_export_hashes.items():
        if reconstructed.get(field) != sha256(path):
            raise ValueError(f"reconstructed result/{field} mismatch")

    git_commit = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
    ).strip()
    git_dirty = bool(
        subprocess.check_output(
            ["git", "-C", str(ROOT), "status", "--porcelain"], text=True
        ).strip()
    )
    z3_cli_version = subprocess.check_output(
        ["z3", "--version"], text=True
    ).strip()
    historical_files = [
        ROOT / "countcegar.py",
        ROOT / "cegar.py",
        ROOT / "verify.py",
        ROOT / "results/countcegar_K4.json",
        ROOT / "results/countcegar_K4.log",
        historical_pool_path,
    ]
    reconstructed_files = [
        complete_pool_path,
        reconstruction_run_path,
        reconstructed_result_path,
        ROOT / "results/countcegar_K4_reconstruction.jsonl",
        cp_model_path,
        cp_response_path,
        cp_stats_path,
        smt2_path,
        z3_result_path,
        sat_cnf_path,
        sat_result_path,
        sat_replay_path,
        sat_differential_path,
        boundary_path,
        certificate_metadata_path,
        proof_path,
        *certificate_logs,
    ]
    source_files = [
        HERE / "README.md",
        HERE / "requirements.txt",
        HERE / "reconstruct.py",
        HERE / "check_z3.py",
        HERE / "check_sat.py",
        HERE / "replay_sat.py",
        HERE / "test_slot_boundary.py",
        HERE / "test_sat_differential.py",
        HERE / "verify_drat.py",
        HERE / "make_manifest.py",
    ]
    manifest = {
        "schema": 1,
        "generated_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "claim": (
            "every 4x7 valuation matrix over {1,2,3,4} has at least "
            "4 EFX0 allocations"
        ),
        "git_commit_at_manifest": git_commit,
        "git_worktree_dirty_at_manifest": git_dirty,
        "git_note": (
            "the commit identifies the base tree; per-file hashes below "
            "identify the exact archived inputs and sources"
        ),
        "historical_run": {
            "status": "incomplete retained terminal master",
            "reported_terminal_pool_size": 1295,
            "retained_pool_size": len(historical_pool),
            "retained_unique_pool_size": len(
                {tuple(assign) for assign in historical_pool}
            ),
            "missing_terminal_entries": 45,
            "exact_terminal_pool_recoverable": False,
            "reason": (
                "the periodic checkpoint predates terminal UNSAT and the "
                "log records neither the final valuations nor cuts"
            ),
            "command": "python countcegar.py --K 4",
            "command_provenance": "inferred from the CLI; not recorded by run",
            "bundle_first_committed_in": (
                "a9c88411593cefe464a0731cd15bc1d03ae97d31"
            ),
            "run_source_hash_recorded": False,
            "files": [file_record(path) for path in historical_files],
        },
        "reconstructed_run": {
            "status": reconstructed["status"],
            "relationship_to_historical_run": (
                "fresh alternative terminal pool; not recovery of the "
                "historical final 45 entries"
            ),
            "pool_size": len(complete_pool),
            "unique_pool_size": len(
                {tuple(assign) for assign in complete_pool}
            ),
            "cp_sat_command": reconstructed["command"],
            "pool_generation_command": reconstruction_run["command"],
            "pool_generation_rounds": reconstruction_run[
                "rounds_this_invocation"
            ],
            "pool_generation_seconds": reconstruction_run[
                "seconds_this_invocation"
            ],
            "z3_check": {
                "status": independent["status"],
                "reason_unknown": independent.get("reason_unknown"),
                "evidentiary_role": z3_role,
                "command": independent["command"],
            },
            "optional_z3_cli_command": (
                "z3 -T:10800 sat.threads=4 -smt2 "
                "results/countcegar_K4_complete.smt2"
            ),
            "slot_boundary_command": boundary["command"],
            "parsed_cp_model": {
                "variables": len(terminal_model.Proto().variables),
                "constraints": len(terminal_model.Proto().constraints),
                "source_pool_rebuild": "byte-identical",
            },
            "parsed_cp_solver_response": {
                "status": "INFEASIBLE",
                "wall_time": terminal_response.wall_time,
            },
            "source_pool_smt2_rebuild": "byte-identical",
            "direct_sat_check": {
                "status": direct_sat["status"],
                "command": direct_sat["command"],
                "solver": direct_solver,
                "variables": parsed_cnf.nv,
                "clauses": len(parsed_cnf.clauses),
                "source_pool_dimacs_rebuild": "byte-identical",
                "differential_regression": "PASS",
                "isolated_process_regression": isolated_process,
                "cold_replay": {
                    "status": sat_replay["status"],
                    "command": sat_replay["command"],
                    "solver": replay_solver,
                    "same_solver_statistics": True,
                },
                "drat_certificate": {
                    "status": certificate_checker["status"],
                    "metadata": relative(certificate_metadata_path),
                    "proof": proof_record,
                    "uncompressed_proof": uncompressed,
                    "generator": {
                        "name": generator["name"],
                        "version": generator["version"],
                        "tag": generator["tag"],
                        "commit": generator["commit"],
                        "wall_seconds": generator["wall_seconds"],
                    },
                    "checker": {
                        "name": certificate_checker["name"],
                        "commit": certificate_checker["commit"],
                        "wall_seconds": certificate_checker["wall_seconds"],
                        "resolution_steps": certificate_checker[
                            "resolution_steps"
                        ],
                        "rat_lemmas_in_core": certificate_checker[
                            "rat_lemmas_in_core"
                        ],
                    },
                },
            },
            "trace_replay": trace_replay,
            "files": [file_record(path) for path in reconstructed_files],
        },
        "environment": {
            "python": platform.python_version(),
            "ortools": ortools_version,
            "z3_python": z3.get_version_string(),
            "z3_cli": z3_cli_version,
            "python_sat": pysat.__version__,
            "platform": platform.platform(),
        },
        "trust_boundary": (
            "CpModelProto, CpSolverResponse, DIMACS, and the compressed "
            "binary DRAT preserve exact claim-bearing artifacts; SMT-LIB2 "
            "preserves the auxiliary Z3 input. The independently checkable "
            "DRAT trace removes trust in the SAT solver verdict, while the "
            "semantic conclusion still trusts the CNF translation and a "
            "correct proof checker"
        ),
        "package_files": [file_record(path) for path in source_files],
    }
    output = HERE / "MANIFEST.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "manifest": str(output)}, indent=2))


if __name__ == "__main__":
    run()
