#!/usr/bin/env python3
"""Promote a checked parkability terminal proof to a bound certificate."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

try:
    from . import terminal_cnf, verify_terminal_drat
except ImportError:
    import terminal_cnf
    import verify_terminal_drat


CADICAL_COMMIT = "146207318796f094dcded87349a64f0c6927309e"
DRAT_TRIM_COMMIT = "2e3b2dc0ecf938addbd779d42877b6ed69d9a985"


def load_json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read {label}: {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def file_record(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": terminal_cnf.sha256(path),
    }


def require_fields(value: dict, required: set[str], label: str) -> None:
    missing = required - set(value)
    if missing:
        raise ValueError(f"{label} is missing fields: {sorted(missing)}")


def require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise ValueError(f"{label} is {actual!r}, expected {expected!r}")


def git_output(source: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(
            f"git {' '.join(arguments)} failed for {source}: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def git_bytes(source: Path, *arguments: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(source), *arguments],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(
            f"git {' '.join(arguments)} failed for {source}: "
            f"{completed.stderr.decode(errors='replace').strip()}"
        )
    return completed.stdout


def require_git_commit(source: Path, expected: str, label: str) -> dict:
    actual = git_output(source, "rev-parse", "HEAD")
    require_equal(actual, expected, f"{label} source commit")
    dirty = git_output(source, "status", "--porcelain", "--untracked-files=no")
    if dirty:
        raise ValueError(f"{label} tracked source files are not clean:\n{dirty}")
    return {
        "source_path": str(source.resolve()),
        "repository": git_output(source, "remote", "get-url", "origin"),
        "commit": actual,
    }


def require_clean_sources(repo: Path, paths: list[Path]) -> str:
    relative = []
    for path in paths:
        resolved = path.resolve()
        try:
            relative.append(str(resolved.relative_to(repo.resolve())))
        except ValueError as error:
            raise ValueError(f"source is outside repository: {path}") from error
    for path in relative:
        git_output(repo, "ls-files", "--error-unmatch", "--", path)
    dirty = git_output(repo, "status", "--porcelain", "--", *relative)
    if dirty:
        raise ValueError(f"certificate sources are not clean:\n{dirty}")
    return git_output(repo, "rev-parse", "HEAD")


def executable_version(executable: Path) -> str:
    completed = subprocess.run(
        [str(executable.resolve()), "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return "not reported"
    return (completed.stdout + completed.stderr).strip()


def rebuild_drat_trim(source: Path, executable: Path) -> dict:
    compiler_name = shutil.which("gcc")
    if compiler_name is None:
        raise FileNotFoundError("gcc is required to reproduce drat-trim")
    compiler = Path(compiler_name).resolve()
    source_bytes = git_bytes(source, "show", f"{DRAT_TRIM_COMMIT}:drat-trim.c")
    with tempfile.TemporaryDirectory(
        prefix="parkability-drat-trim-rebuild-"
    ) as directory_name:
        directory = Path(directory_name)
        source_snapshot = directory / "drat-trim.c"
        rebuilt = directory / "drat-trim"
        source_snapshot.write_bytes(source_bytes)
        command = [
            str(compiler),
            "drat-trim.c",
            "-std=c99",
            "-O2",
            "-o",
            "drat-trim",
        ]
        completed = subprocess.run(
            command,
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "fresh drat-trim build failed\n" + completed.stdout + completed.stderr
            )
        rebuilt_record = file_record(rebuilt)
        require_equal(
            rebuilt_record["sha256"],
            terminal_cnf.sha256(executable),
            "fresh drat-trim build hash",
        )
        compiler_version = subprocess.run(
            [str(compiler), "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "status": "BYTE_IDENTICAL",
            "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "command": command,
            "compiler": {
                **file_record(compiler),
                "version": (
                    compiler_version.stdout + compiler_version.stderr
                ).splitlines()[0],
            },
            "rebuilt_executable_sha256": rebuilt_record["sha256"],
        }


def certify(args: argparse.Namespace) -> dict:
    inputs = [
        args.pool,
        args.terminal_result,
        args.dimacs,
        args.replay_result,
        args.proof_generation,
        args.proof,
        args.proof_check,
        args.cadical,
        args.drat_trim,
    ]
    if args.certificate_out.resolve() in {path.resolve() for path in inputs}:
        raise ValueError("certificate output must be distinct from every input")

    snapshot = terminal_cnf.load_pool_snapshot(args.pool)
    terminal = load_json(args.terminal_result, "terminal result")
    replay = load_json(args.replay_result, "cold replay result")
    proof_generation = load_json(args.proof_generation, "DRAT generation result")
    proof_check = load_json(args.proof_check, "DRAT check result")
    dimacs_record = file_record(args.dimacs)
    proof_record = file_record(args.proof)

    require_fields(
        terminal,
        {
            "schema",
            "status",
            "solver",
            "pool_sha256",
            "pool_canonical_sha256",
            "pool_size",
            "dimacs_sha256",
            "dimacs_bytes",
            "variables",
            "clauses",
            "source_sha256",
        },
        "terminal result",
    )
    require_equal(
        terminal["schema"],
        "parkability-terminal-cnf-result-v1",
        "terminal schema",
    )
    require_equal(terminal["status"], "UNSAT_SOLVER_RESULT", "terminal status")
    require_equal(terminal["solver"].get("status"), "UNSAT", "terminal solver status")
    require_equal(
        terminal["pool_sha256"], snapshot.contents_sha256, "terminal pool hash"
    )
    require_equal(
        terminal["pool_canonical_sha256"],
        terminal_cnf.canonical_sha256(snapshot.document),
        "terminal canonical pool hash",
    )
    require_equal(terminal["pool_size"], len(snapshot.triples), "terminal pool size")
    require_equal(
        terminal["dimacs_sha256"], dimacs_record["sha256"], "terminal DIMACS hash"
    )
    require_equal(
        terminal["dimacs_bytes"], dimacs_record["bytes"], "terminal DIMACS size"
    )

    require_fields(
        replay,
        {
            "schema",
            "status",
            "solver",
            "dimacs_sha256",
            "dimacs_bytes",
            "variables",
            "clauses",
            "source_sha256",
        },
        "cold replay result",
    )
    require_equal(
        replay["schema"],
        "parkability-terminal-cnf-replay-v1",
        "cold replay schema",
    )
    require_equal(replay["status"], "UNSAT_SOLVER_RESULT", "cold replay status")
    require_equal(replay["solver"].get("status"), "UNSAT", "cold replay solver status")
    for field in ("dimacs_sha256", "dimacs_bytes", "variables", "clauses"):
        require_equal(replay[field], terminal[field], f"replay {field}")

    require_fields(
        proof_generation,
        {
            "schema",
            "status",
            "terminal_result",
            "input",
            "proof",
            "generator",
            "source_sha256",
        },
        "DRAT generation result",
    )
    require_equal(
        proof_generation["schema"],
        "parkability-terminal-drat-generation-v1",
        "DRAT generation schema",
    )
    require_equal(
        proof_generation["status"],
        "UNSAT_PROOF_GENERATED",
        "DRAT generation status",
    )
    require_equal(
        proof_generation["terminal_result"].get("sha256"),
        terminal_cnf.sha256(args.terminal_result),
        "DRAT generation terminal-result hash",
    )
    require_equal(
        proof_generation["input"].get("sha256"),
        dimacs_record["sha256"],
        "DRAT generation input hash",
    )
    require_equal(
        proof_generation["input"].get("bytes"),
        dimacs_record["bytes"],
        "DRAT generation input size",
    )
    generated_proof = proof_generation["proof"]
    if not isinstance(generated_proof, dict):
        raise ValueError("DRAT generation result has no proof record")

    require_fields(
        proof_check,
        {
            "schema",
            "status",
            "terminal_result",
            "input",
            "proof",
            "checker",
            "source_sha256",
        },
        "DRAT check result",
    )
    require_equal(
        proof_check["schema"],
        "parkability-terminal-drat-check-v1",
        "DRAT check schema",
    )
    require_equal(proof_check["status"], "VERIFIED_DRAT", "DRAT check status")
    require_equal(
        proof_check["terminal_result"].get("sha256"),
        terminal_cnf.sha256(args.terminal_result),
        "DRAT terminal-result hash",
    )
    require_equal(
        proof_check["terminal_result"].get("pool_sha256"),
        snapshot.contents_sha256,
        "DRAT terminal-result pool hash",
    )
    require_equal(
        proof_check["input"].get("sha256"),
        dimacs_record["sha256"],
        "DRAT input hash",
    )
    require_equal(
        proof_check["input"].get("bytes"),
        dimacs_record["bytes"],
        "DRAT input size",
    )
    require_equal(
        proof_check["proof"].get("source_sha256"),
        proof_record["sha256"],
        "DRAT proof hash",
    )
    require_equal(
        proof_check["proof"].get("source_bytes"),
        proof_record["bytes"],
        "DRAT proof size",
    )
    require_equal(
        generated_proof.get("sha256"),
        proof_check["proof"].get("uncompressed_sha256"),
        "generated/uncompressed proof hash",
    )
    require_equal(
        generated_proof.get("bytes"),
        proof_check["proof"].get("uncompressed_bytes"),
        "generated/uncompressed proof size",
    )
    require_equal(proof_check["checker"].get("exit_code"), 0, "checker exit code")
    require_equal(
        proof_check["checker"].get("reported_verified"),
        True,
        "checker verification flag",
    )
    require_equal(
        proof_check["checker"].get("sha256"),
        terminal_cnf.sha256(args.drat_trim),
        "checker executable hash",
    )

    source_files = {
        "terminal_encoder": Path(__file__).with_name("terminal_cnf.py"),
        "cold_replay": Path(__file__).with_name("replay_terminal_cnf.py"),
        "proof_generator": Path(__file__).with_name("generate_terminal_drat.py"),
        "proof_verifier": Path(__file__).with_name("verify_terminal_drat.py"),
        "certificate_finalizer": Path(__file__).resolve(),
    }
    require_equal(
        terminal["source_sha256"],
        terminal_cnf.sha256(source_files["terminal_encoder"]),
        "terminal encoder source hash",
    )
    require_equal(
        replay["source_sha256"],
        terminal_cnf.sha256(source_files["cold_replay"]),
        "cold replay source hash",
    )
    require_equal(
        proof_generation["source_sha256"],
        terminal_cnf.sha256(source_files["proof_generator"]),
        "proof generator source hash",
    )
    require_equal(
        proof_check["source_sha256"],
        terminal_cnf.sha256(source_files["proof_verifier"]),
        "proof verifier source hash",
    )
    source_commit = require_clean_sources(args.repo, list(source_files.values()))
    with tempfile.TemporaryDirectory(
        prefix="parkability-terminal-rebuild-"
    ) as directory_name:
        rebuilt_cnf, _, _ = terminal_cnf.build_master(
            snapshot.document, snapshot.triples
        )
        rebuilt_path = Path(directory_name) / "terminal.cnf"
        terminal_cnf.export_dimacs(rebuilt_cnf, rebuilt_path)
        rebuilt_record = file_record(rebuilt_path)
        require_equal(
            rebuilt_record["sha256"],
            dimacs_record["sha256"],
            "deterministic terminal DIMACS rebuild hash",
        )
        require_equal(
            rebuilt_record["bytes"],
            dimacs_record["bytes"],
            "deterministic terminal DIMACS rebuild size",
        )
        require_equal(rebuilt_cnf.nv, terminal["variables"], "rebuilt variable count")
        require_equal(
            len(rebuilt_cnf.clauses),
            terminal["clauses"],
            "rebuilt clause count",
        )

    cadical = require_git_commit(args.cadical_source, CADICAL_COMMIT, "CaDiCaL")
    require_equal(
        args.cadical.resolve(),
        (args.cadical_source / "build" / "cadical").resolve(),
        "CaDiCaL build-output path",
    )
    cadical.update(
        {
            "name": "CaDiCaL",
            "version": executable_version(args.cadical),
            "executable": file_record(args.cadical),
            "role": "proof generator; not trusted for the checked conclusion",
        }
    )
    require_equal(
        proof_generation["generator"].get("commit"),
        CADICAL_COMMIT,
        "proof generator commit",
    )
    require_equal(
        proof_generation["generator"].get("executable_sha256"),
        cadical["executable"]["sha256"],
        "proof generator executable hash",
    )
    checker = require_git_commit(args.drat_trim_source, DRAT_TRIM_COMMIT, "drat-trim")
    require_equal(
        args.drat_trim.resolve(),
        (args.drat_trim_source / "drat-trim").resolve(),
        "drat-trim build-output path",
    )
    checker.update(
        {
            "name": "drat-trim",
            "executable": file_record(args.drat_trim),
            "role": "proof checker",
            "reproducible_build": rebuild_drat_trim(
                args.drat_trim_source, args.drat_trim
            ),
        }
    )
    with tempfile.TemporaryDirectory(
        prefix="parkability-terminal-final-proof-check-"
    ) as directory_name:
        final_check_path = Path(directory_name) / "proof-check.json"
        with contextlib.redirect_stdout(io.StringIO()):
            final_check_exit = verify_terminal_drat.run(
                argparse.Namespace(
                    dimacs=args.dimacs,
                    terminal_result=args.terminal_result,
                    proof=args.proof,
                    result_out=final_check_path,
                    expect_dimacs_sha256=dimacs_record["sha256"],
                    expect_proof_sha256=proof_record["sha256"],
                    expect_uncompressed_sha256=proof_check["proof"][
                        "uncompressed_sha256"
                    ],
                    expect_uncompressed_bytes=proof_check["proof"][
                        "uncompressed_bytes"
                    ],
                    checker=str(args.drat_trim),
                    expect_checker_sha256=checker["executable"]["sha256"],
                    timeout_seconds=args.checker_timeout_seconds,
                    binary=proof_check["proof"]["format"] == "binary DRAT",
                    hash_only=False,
                )
            )
        final_proof_check = load_json(final_check_path, "final DRAT recheck")
        require_equal(final_check_exit, 0, "final DRAT checker exit")
        require_equal(
            final_proof_check.get("status"),
            "VERIFIED_DRAT",
            "final DRAT recheck status",
        )

    for field in ("n", "m", "lower", "upper", "symmetry"):
        require_equal(
            terminal.get(field),
            snapshot.document[field],
            f"terminal {field}",
        )
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("repository source commit is not a full Git object ID")
    require_equal(
        require_clean_sources(args.repo, list(source_files.values())),
        source_commit,
        "repository source commit after certification",
    )

    result = {
        "schema": "parkability-terminal-certificate-v1",
        "status": "CERTIFIED_UNSAT",
        "claim": (
            f"every additive {snapshot.document['n']}x{snapshot.document['m']} "
            f"valuation matrix with entries in "
            f"[{snapshot.document['lower']},{snapshot.document['upper']}] "
            "has a parkable deletion triple"
        ),
        "claim_boundary": (
            "this certifies the bounded parkability statement, not additive "
            "EFX existence outside this route or outside the value box"
        ),
        "logic_chain": [
            "strict pool parsing",
            "independent threshold-CNF translation",
            "byte-identical terminal CNF rebuild",
            "direct UNSAT solver result",
            "cold solve of frozen DIMACS",
            "externally checked DRAT proof",
        ],
        "pool": {
            **file_record(args.pool),
            "canonical_sha256": terminal_cnf.canonical_sha256(snapshot.document),
            "triples": len(snapshot.triples),
            "n": snapshot.document["n"],
            "m": snapshot.document["m"],
            "lower": snapshot.document["lower"],
            "upper": snapshot.document["upper"],
            "symmetry": snapshot.document["symmetry"],
        },
        "dimacs": {
            **dimacs_record,
            "variables": terminal["variables"],
            "clauses": terminal["clauses"],
            "rebuild_sha256": rebuilt_record["sha256"],
        },
        "proof": {
            **proof_record,
            "format": proof_check["proof"]["format"],
            "compression": proof_check["proof"]["compression"],
            "uncompressed_bytes": proof_check["proof"]["uncompressed_bytes"],
            "uncompressed_sha256": proof_check["proof"]["uncompressed_sha256"],
        },
        "records": {
            "terminal_result": file_record(args.terminal_result),
            "cold_replay": file_record(args.replay_result),
            "proof_generation": file_record(args.proof_generation),
            "proof_check": file_record(args.proof_check),
            "final_proof_recheck": final_proof_check,
        },
        "toolchain": {
            "generator": cadical,
            "checker": checker,
        },
        "source": {
            "repository": str(args.repo.resolve()),
            "commit": source_commit,
            "files": {name: file_record(path) for name, path in source_files.items()},
        },
    }
    terminal_cnf.atomic_json(args.certificate_out, result)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--terminal-result", type=Path, required=True)
    parser.add_argument("--dimacs", type=Path, required=True)
    parser.add_argument("--replay-result", type=Path, required=True)
    parser.add_argument("--proof-generation", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--proof-check", type=Path, required=True)
    parser.add_argument("--certificate-out", type=Path, required=True)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--cadical-source", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--drat-trim-source", type=Path, required=True)
    parser.add_argument("--checker-timeout-seconds", type=int, default=10800)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    if args.checker_timeout_seconds <= 0:
        parser.error("checker-timeout-seconds must be positive")
    return args


def main() -> None:
    result = certify(parse_args())
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
