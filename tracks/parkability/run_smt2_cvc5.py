#!/usr/bin/env python3
"""Replay an SMT-LIB QF_LRA artifact with the independent cvc5 solver."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path

import cvc5


def atomic_json(path, payload):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


SCHEMA = "cvc5-smt2-replay-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source, output, timeout_seconds, model_output):
    solver = cvc5.Solver()
    source_text = source.read_text()
    declared_logics = re.findall(r"\(set-logic\s+([^\s()]+)\)", source_text)
    if len(declared_logics) > 1:
        raise ValueError("source declares more than one logic")
    logic = declared_logics[0] if declared_logics else "QF_LRA"
    if logic != "QF_LRA":
        raise ValueError(f"expected QF_LRA, found {logic}")
    if not declared_logics:
        solver.setLogic(logic)
    solver.setOption("produce-models", "true")
    solver.setOption("tlimit-per", str(timeout_seconds * 1000))
    parser = cvc5.InputParser(solver)
    parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6, str(source))
    started = time.time()
    responses = []
    verdict = None
    while not parser.done():
        command = parser.nextCommand()
        if command.isNull():
            break
        response = command.invoke(solver, parser.getSymbolManager()).strip()
        if response:
            responses.append(
                {"command": command.getCommandName(), "response": response}
            )
        if command.getCommandName() == "check-sat":
            verdict = response
    model_path = None
    if verdict == "sat" and model_output is not None:
        terms = parser.getSymbolManager().getDeclaredTerms()
        model_output.write_text(solver.getModel([], terms))
        model_path = str(model_output)
    result = {
        "schema": SCHEMA,
        "status": verdict.upper() if verdict else "NO_CHECK_SAT_RESPONSE",
        "meaning": (
            "Independent cvc5 replay of the exact SMT-LIB formula. SAT or "
            "UNSAT is a solver verdict; UNKNOWN is not a theorem verdict."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "solver": "cvc5",
        "solver_version": cvc5.__version__,
        "logic": logic,
        "timeout_seconds": timeout_seconds,
        "elapsed_seconds": round(time.time() - started, 6),
        "responses": responses,
        "model_output": model_path,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--model-output", type=Path)
    args = parser.parse_args()
    result = run(
        args.source, args.output, args.timeout_seconds, args.model_output
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
