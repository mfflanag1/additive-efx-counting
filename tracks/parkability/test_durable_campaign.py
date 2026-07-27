#!/usr/bin/env python3
"""Tests for the fixed K=4 durable campaign supervisor."""

from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

try:
    from . import durable_campaign
except ImportError:
    import durable_campaign


FAKE_RUNNER = r"""#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--K", type=int, required=True)
parser.add_argument("--add", type=int, required=True)
parser.add_argument("--time-limit", type=float, required=True)
parser.add_argument("--workers", type=int, required=True)
parser.add_argument("--random-seed", type=int, required=True)
parser.add_argument("--symmetry", required=True)
parser.add_argument("--max-iterations", type=int, required=True)
parser.add_argument("--pool", type=Path, required=True)
parser.add_argument("--trace", type=Path, required=True)
parser.add_argument("--result", type=Path, required=True)
args = parser.parse_args()

mode = os.environ.get("DURABLE_FAKE_MODE", "normal")
print("ENTERED", flush=True)
if mode == "sleep":
    time.sleep(1.0)
if mode == "sleep_long":
    time.sleep(30.0)
if mode == "nonzero":
    print("deliberate child failure", flush=True)
    raise SystemExit(7)

pool = json.loads(args.pool.read_text())
starting_pool_size = len(pool["triples"])
if starting_pool_size == 0:
    pool["triples"].append({
        "floater": 0,
        "base_owner": [None, 0, 0, 0, 0, 0, 0, 0],
        "host": 0,
    })
    status = "MASTER_UNKNOWN"
else:
    status = "UNSAT_CANDIDATE"
args.pool.write_text(json.dumps(pool, indent=2, sort_keys=True) + "\n")
args.trace.write_text(json.dumps({"fake": True, "status": status}) + "\n")
pool_bytes = args.pool.read_bytes()
trace_bytes = args.trace.read_bytes()
result = {
    "schema": "parkable-deletion-cegar-result-v1",
    "property": "zero_parkable_deletion_triples",
    "status": status,
    "n": 4,
    "m": 8,
    "lower": 1,
    "upper": args.K,
    "symmetry": args.symmetry,
    "iterations": 1,
    "pool_size": len(pool["triples"]),
    "pool_path": str(args.pool.resolve()),
    "pool_sha256": hashlib.sha256(pool_bytes).hexdigest(),
    "trace_path": str(args.trace.resolve()),
    "trace_sha256": hashlib.sha256(trace_bytes).hexdigest(),
    "run_config": {
        "add_per_iteration": args.add,
        "time_limit_seconds_per_master": args.time_limit,
        "workers": args.workers,
        "random_seed": args.random_seed,
        "max_iterations": args.max_iterations,
        "starting_pool_size": starting_pool_size,
    },
}
args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(status, flush=True)
"""


def run_git(arguments: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def make_source(root: Path) -> tuple[Path, Path]:
    source = root / "source"
    source.mkdir()
    runner = source / "run_cegar.py"
    runner.write_text(FAKE_RUNNER)
    run_git(["init", "-q"], source)
    run_git(["config", "user.name", "Durable Test"], source)
    run_git(["config", "user.email", "durable@example.invalid"], source)
    run_git(
        ["remote", "add", "origin", "https://github.com/example/private-test.git"],
        source,
    )
    run_git(["add", "run_cegar.py"], source)
    run_git(["commit", "-q", "-m", "fixture"], source)
    return source, runner


def file_hashes(directory: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in directory.iterdir()
        if path.is_file()
    }


def expect_error(error_type: type[Exception], callback: object) -> None:
    try:
        callback()
    except error_type:
        return
    raise AssertionError(f"expected {error_type.__name__}")


def test_lifecycle(base: Path, source: Path, runner: Path) -> int:
    root = base / "lifecycle"
    first = durable_campaign.run_campaign_session(root, source, runner, sys.executable)
    if (
        first["status"] != "CHILD_RESULT_RECORDED"
        or first["child_result_status"] != "MASTER_UNKNOWN"
        or first["terminal"]
    ):
        raise AssertionError("first resumable session was recorded incorrectly")
    campaign = json.loads((root / "campaign.json").read_text())
    if campaign["config"] != durable_campaign.FIXED_CONFIG:
        raise AssertionError("fixed campaign configuration changed")
    if not campaign["identity"]["source"]["clean"]:
        raise AssertionError("clean source state was not recorded")
    if campaign["identity"]["source"]["remote"] != (
        "https://github.com/example/private-test.git"
    ):
        raise AssertionError("source remote was not recorded")
    if campaign["identity"]["dependencies"]["ortools"] is None:
        raise AssertionError("OR-Tools dependency version was not recorded")

    first_session = root / "sessions" / "000001"
    frozen_hashes = file_hashes(first_session)
    ready = durable_campaign.campaign_status(root)
    if ready["status"] != "READY" or ready["session_count"] != 1:
        raise AssertionError("resumable campaign status is wrong")

    second = durable_campaign.run_campaign_session(root, source, runner, sys.executable)
    if (
        second["status"] != "CHILD_RESULT_RECORDED"
        or second["child_result_status"] != "UNSAT_CANDIDATE"
        or not second["terminal"]
    ):
        raise AssertionError("terminal session was recorded incorrectly")
    if file_hashes(first_session) != frozen_hashes:
        raise AssertionError("a completed session was modified during resume")
    second_session = root / "sessions" / "000002"
    if (first_session / "pool.after.json").read_bytes() != (
        second_session / "pool.before.json"
    ).read_bytes():
        raise AssertionError("pool snapshots do not form an exact resume chain")
    state = durable_campaign.inspect_campaign(root)
    if state["session_count"] != 2 or not state["terminal"]:
        raise AssertionError("terminal campaign inspection is wrong")
    if durable_campaign.campaign_status(root)["status"] != "TERMINAL":
        raise AssertionError("terminal status command is wrong")
    expect_error(
        durable_campaign.TerminalCampaign,
        lambda: durable_campaign.run_campaign_session(
            root, source, runner, sys.executable
        ),
    )
    return 10


def test_whole_session_lock(base: Path, source: Path, runner: Path) -> int:
    root = base / "lock"
    errors: list[BaseException] = []

    def worker() -> None:
        try:
            durable_campaign.run_campaign_session(root, source, runner, sys.executable)
        except BaseException as error:
            errors.append(error)

    os.environ["DURABLE_FAKE_MODE"] = "sleep"
    thread = threading.Thread(target=worker)
    thread.start()
    log_path = root / "sessions" / "000001" / "child.log"
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if log_path.exists() and "ENTERED" in log_path.read_text():
            break
        time.sleep(0.02)
    else:
        raise AssertionError("fake child did not enter")
    try:
        if durable_campaign.campaign_status(root)["status"] != "RUNNING":
            raise AssertionError("status did not report the active session")
        expect_error(
            durable_campaign.CampaignAlreadyRunning,
            lambda: durable_campaign.run_campaign_session(
                root, source, runner, sys.executable
            ),
        )
    finally:
        thread.join(timeout=10)
        os.environ.pop("DURABLE_FAKE_MODE", None)
    if thread.is_alive() or errors:
        raise AssertionError(f"locked worker failed: {errors!r}")
    return 3


def test_abnormal_child(base: Path, source: Path, runner: Path) -> int:
    root = base / "nonzero"
    os.environ["DURABLE_FAKE_MODE"] = "nonzero"
    try:
        end = durable_campaign.run_campaign_session(
            root, source, runner, sys.executable
        )
    finally:
        os.environ.pop("DURABLE_FAKE_MODE", None)
    if end["status"] != "CHILD_NONZERO" or end["returncode"] != 7:
        raise AssertionError("nonzero child was not recorded")
    if end["artifacts"]["log"] is None or end["artifacts"]["pool_after"] is None:
        raise AssertionError("abnormal session artifacts were not archived")
    if durable_campaign.campaign_status(root)["status"] != "READY":
        raise AssertionError("intact nonzero session is not resumable")
    resumed = durable_campaign.run_campaign_session(
        root, source, runner, sys.executable
    )
    if resumed["child_result_status"] != "MASTER_UNKNOWN":
        raise AssertionError("campaign did not resume after a nonzero child")
    return 4


def test_signal_forwarding(base: Path, source: Path, runner: Path) -> int:
    root = base / "signal"
    errors: list[BaseException] = []

    def terminate_after_entry() -> None:
        try:
            log_path = root / "sessions" / "000001" / "child.log"
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                if log_path.exists() and "ENTERED" in log_path.read_text():
                    os.kill(os.getpid(), signal.SIGTERM)
                    return
                time.sleep(0.02)
            raise AssertionError("fake child did not enter before signal")
        except BaseException as error:
            errors.append(error)

    os.environ["DURABLE_FAKE_MODE"] = "sleep_long"
    sender = threading.Thread(target=terminate_after_entry)
    sender.start()
    try:
        end = durable_campaign.run_campaign_session(
            root, source, runner, sys.executable
        )
    finally:
        sender.join(timeout=10)
        os.environ.pop("DURABLE_FAKE_MODE", None)
    if sender.is_alive() or errors:
        raise AssertionError(f"signal sender failed: {errors!r}")
    if (
        end["status"] != "CHILD_SIGNAL"
        or end["returncode"] != -signal.SIGTERM
        or end["signal"] != "SIGTERM"
        or not isinstance(end["child_pid"], int)
    ):
        raise AssertionError("SIGTERM was not forwarded and recorded")
    if durable_campaign.campaign_status(root)["status"] != "READY":
        raise AssertionError("signalled campaign is not safely resumable")
    return 3


def test_supervisor_kill_recovery(base: Path, source: Path, runner: Path) -> int:
    root = base / "supervisor-kill"
    environment = os.environ.copy()
    environment["DURABLE_FAKE_MODE"] = "sleep"
    supervisor = subprocess.Popen(
        [
            sys.executable,
            str(Path(durable_campaign.__file__).resolve()),
            "run",
            "--root",
            str(root),
            "--repo-root",
            str(source),
            "--runner",
            str(runner),
            "--python",
            sys.executable,
        ],
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    log_path = root / "sessions" / "000001" / "child.log"
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if log_path.exists() and "ENTERED" in log_path.read_text():
            break
        if supervisor.poll() is not None:
            raise AssertionError("supervisor exited before its child entered")
        time.sleep(0.02)
    else:
        supervisor.kill()
        raise AssertionError("fake child did not enter before supervisor kill")

    os.kill(supervisor.pid, signal.SIGKILL)
    supervisor.wait(timeout=5)
    if supervisor.returncode != -signal.SIGKILL:
        raise AssertionError("supervisor was not killed as requested")
    if durable_campaign.campaign_status(root)["status"] != "RUNNING":
        raise AssertionError("orphaned child did not retain the campaign lock")

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        status = durable_campaign.campaign_status(root)
        if status["status"] == "RECOVERY_REQUIRED":
            break
        time.sleep(0.05)
    else:
        raise AssertionError("completed orphaned session did not become recoverable")

    resumed = durable_campaign.run_campaign_session(
        root, source, runner, sys.executable
    )
    recovered = json.loads((root / "sessions" / "000001" / "end.json").read_text())
    if (
        recovered["status"] != "RECOVERED_CHILD_RESULT"
        or recovered["recovered"] is not True
        or recovered["child_result_status"] != "MASTER_UNKNOWN"
    ):
        raise AssertionError("orphaned child result was not recovered")
    if (
        resumed["child_result_status"] != "UNSAT_CANDIDATE"
        or durable_campaign.campaign_status(root)["status"] != "TERMINAL"
    ):
        raise AssertionError("campaign did not resume after hard-kill recovery")
    return 5


def test_corruption(base: Path, source: Path, runner: Path) -> int:
    root = base / "corruption"
    durable_campaign.run_campaign_session(root, source, runner, sys.executable)
    snapshot = root / "sessions" / "000001" / "pool.after.json"
    snapshot.write_bytes(snapshot.read_bytes() + b"\n")
    expect_error(
        durable_campaign.CampaignError,
        lambda: durable_campaign.run_campaign_session(
            root, source, runner, sys.executable
        ),
    )
    status = durable_campaign.campaign_status(root)
    if status["status"] != "CORRUPT" or "mismatch" not in status["error"]:
        raise AssertionError("snapshot corruption was not reported")
    return 2


def main() -> None:
    if (
        durable_campaign.campaign_status(
            Path(tempfile.gettempdir()) / "durable-campaign-does-not-exist"
        )["status"]
        != "NOT_INITIALIZED"
    ):
        raise AssertionError("uninitialized status is wrong")
    with tempfile.TemporaryDirectory(
        prefix="parkability-durable-test-"
    ) as directory_name:
        base = Path(directory_name)
        source, runner = make_source(base)
        checks = 1
        checks += test_lifecycle(base, source, runner)
        checks += test_whole_session_lock(base, source, runner)
        checks += test_abnormal_child(base, source, runner)
        checks += test_signal_forwarding(base, source, runner)
        checks += test_supervisor_kill_recovery(base, source, runner)
        checks += test_corruption(base, source, runner)
    print(f"PASS durable K=4 campaign supervisor: {checks} checks")


if __name__ == "__main__":
    main()
