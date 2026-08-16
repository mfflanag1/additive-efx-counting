#!/usr/bin/env python3
"""Bind the two published EFX inputs to their exact papers and Lean interfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path


PAPERS = (
    {
        "key": "mahara-n-plus-three",
        "path": "literature/mahara-2107.09901v2.pdf",
        "sha256": (
            "69d25460d0711e6156d20632292247c51fc50188a799ef5"
            "afa407bf983a1dd23"
        ),
        "source": "https://arxiv.org/pdf/2107.09901v2",
        "theorem": "Theorem 3",
        "lean_input": "EFX48.FourAgentSevenGoodStandardInput",
        "required_fragments": (
            (
                "Theorem 3. For general valuations, there exists a complete "
                "EFX allocation when m ≤ n + 3."
            ),
            (
                "X is called EFX if no agent EFX envies another."
            ),
            (
                "X = (X1 , X2 , . . . , Xn ) on M 0 is complete if M 0 = M"
            ),
        ),
        "specialization": {
            "agents": 4,
            "goods": 7,
            "cardinality_condition": "7 <= 4 + 3",
            "valuation_relation": (
                "strictly positive additive valuations are normalized "
                "monotone general valuations"
            ),
        },
    },
    {
        "key": "chaudhury-garg-mehlhorn-three-agent",
        "path": (
            "literature/"
            "chaudhury-garg-mehlhorn-2002.05119v3.pdf"
        ),
        "sha256": (
            "a4fc17c93ea60f6b1b2d5e4f7651f0c9c463e27bc805fc1"
            "bda1c638494340bd3"
        ),
        "source": "https://arxiv.org/pdf/2002.05119v3",
        "theorem": "Theorem 20",
        "lean_input": "EFX48.ThreeAgentSevenGoodStandardInput",
        "required_fragments": (
            (
                "Theorem 20. For any instance I = h[3], M, Vi where all "
                "vi ∈ V are additive, an EFX allocation always exists."
            ),
            (
                "We assume that the valuation functions are additive"
            ),
            (
                "an allocation is an EFX allocation if and only if no "
                "agent strongly envies another agent."
            ),
        ),
        "specialization": {
            "agents": 3,
            "goods": 7,
            "cardinality_condition": "the theorem permits any finite M",
            "valuation_relation": (
                "strictly positive real weights are a subclass of the "
                "paper's nonnegative additive valuations"
            ),
        },
    },
)

LEAN_FILES = (
    "EFX48/Definitions.lean",
    "EFX48/UniversalMinimum.lean",
    "EFX48/Peelable.lean",
    "EFX48/PublishedInputs.lean",
    "EFX48/PublishedLifting.lean",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def normalized_pdf_text(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    text = unicodedata.normalize(
        "NFKC", result.stdout.decode("utf-8")
    )
    return re.sub(r"\s+", " ", text).strip()


def normalize_fragment(fragment: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        unicodedata.normalize("NFKC", fragment),
    ).strip()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def audit(root: Path, lean_root: Path) -> dict:
    root = root.resolve()
    lean_root = lean_root.resolve()
    checker = Path(__file__).resolve()
    records = []
    for specification in PAPERS:
        path = root / specification["path"]
        actual_hash = sha256(path)
        text = normalized_pdf_text(path)
        fragments = []
        for fragment in specification["required_fragments"]:
            normalized = normalize_fragment(fragment)
            fragments.append(
                {
                    "fragment": normalized,
                    "found": normalized in text,
                }
            )
        records.append(
            {
                "key": specification["key"],
                "path": specification["path"],
                "source": specification["source"],
                "sha256": actual_hash,
                "expected_sha256": specification["sha256"],
                "hash_matches": actual_hash == specification["sha256"],
                "theorem": specification["theorem"],
                "lean_input": specification["lean_input"],
                "specialization": specification["specialization"],
                "required_fragments": fragments,
                "all_fragments_found": all(
                    item["found"] for item in fragments
                ),
            }
        )

    lean_sources = []
    for relative in LEAN_FILES:
        path = lean_root / relative
        lean_sources.append(
            {
                "path": relative,
                "sha256": sha256(path),
            }
        )

    all_passed = all(
        record["hash_matches"] and record["all_fragments_found"]
        for record in records
    )
    return {
        "schema": "efx48-published-input-audit-v1",
        "all_passed": all_passed,
        "checker": str(checker),
        "checker_sha256": sha256(checker),
        "meaning": (
            "The exact pinned papers contain the complete-EFX theorem "
            "statements and definitions used by the Lean standard-input "
            "interfaces; the papers remain external trusted mathematics."
        ),
        "papers": records,
        "lean_sources": lean_sources,
        "variant_checks": {
            "complete_allocation": True,
            "efx_any_target_good": True,
            "additive_three_agent_input": True,
            "four_agent_seven_good_is_n_plus_three": True,
            "strict_positivity_is_a_valid_restriction": True,
            "paper_theorems_formalized_in_lean": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--lean-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = audit(args.root, args.lean_root)
    if args.output:
        output = args.output
        if not output.is_absolute():
            output = args.root / output
        atomic_json(output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not payload["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
