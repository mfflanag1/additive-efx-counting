# EFX 4x8 manuscripts

`main.tex` is the original eight-page technical review draft.

`submission.tex` is the expanded submission manuscript. It incorporates the
two independent internal reviews, prints the full conditional Lean interface,
states the hybrid trust boundary precisely, and includes reproducibility and
review appendices.

Build either manuscript with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error submission.tex
```

Rendered copies are written to:

- `../../output/pdf/efx48-review-draft.pdf`
- `../../output/pdf/efx48-submission.pdf`
