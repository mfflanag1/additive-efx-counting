import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_early_r_dual_base_scalar_audit():
    frozen = ROOT / "results/length_three_early_r_dual_base_scalar_audit.json"
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "audit.json"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tracks/parkability/audit_length_three_early_r_dual_base.py"),
                "--output",
                str(output),
            ],
            cwd=ROOT,
            check=True,
        )
        payload = json.loads(output.read_text())
        assert payload["status"] == "ALL_NEGATED_IMPLICATIONS_UNSAT"
        assert len(payload["checks"]) == 4
        assert all(check["negated_status"] == "UNSAT" for check in payload["checks"])
        assert output.read_bytes() == frozen.read_bytes()


if __name__ == "__main__":
    test_early_r_dual_base_scalar_audit()
    print("length-three early-r dual-base scalar audit passed")
