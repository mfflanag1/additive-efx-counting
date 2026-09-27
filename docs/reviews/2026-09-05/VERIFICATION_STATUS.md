# Fresh verification: 5 September 2026

All claim-bearing code and mathematical evidence are copied from the pinned source commit without changes. Only the paper and review-support material were edited.

| Check | Fresh result | Coverage |
|---|---|---|
| Three exact witness counters | PASS, about 84 s including environment launch | Six witnesses; 11,860,961 labeled allocations per implementation; counts 4,5,6,4,4,4 |
| Parking certificates | PASS | All seven archived certificates |
| SAT differential tests | Exit 0; recorded PASS | Threshold/EFX translation and boundary controls; not a substitute for the full theorem |
| Protected-slot boundary tests | Exit 0; expected OPTIMAL/OPTIMAL/INFEASIBLE | Empty pool, three distinct allocations, all four allocations |
| Retained binary DRAT proof | VERIFIED, about 69 s | Full logical replay of the archived finite-box CNF proof, after all hash checks |
| LaTeX build | Exit 0 | Revised specialist-review manuscript |

The proof replay used freshly compiled enclosed drat-trim source. CNF SHA-256: `ccc2aa45a5710d967a166abf7bc56a2026c517f4157730872b99524027baa166`. Decompressed proof SHA-256: `710c51bd36addd3d1ea73c14d902d2b1d9aba23cafcd4874ef1d21daf2779a5b`. The decompressed proof is 134,426,255 bytes; the compressed original remains in the package.

Fresh dependency-bearing replay: Python 3.13.5, Python-SAT 1.9.dev15, Z3 5.1.0, OR-Tools 9.15.6755, macOS arm64. Original requirements retain the historical pins. Full commands, exits and exact timings are in `review-checks/*.run.json`; output and environment details are in the paired logs/results.

Not newly performed: an independent human review, formalization of the encoding, a new full CP-SAT search, or an exhaustive literature/priority determination. A passing DRAT replay proves the supplied CNF unsatisfiable; the mathematical reduction to that CNF remains the specialist's central review obligation.
