PYTHON ?= python3
VERIFY_TMP ?= /tmp/additive-efx-counting-verify

.PHONY: install verify verify-paper verify-audit paper

install:
	$(PYTHON) -m pip install -r requirements.txt

verify: verify-paper verify-audit

verify-paper:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/counting_witnesses/verify_all.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/generalized_parking/verify_certificates.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_k4/test_sat_differential.py --result-out $(VERIFY_TMP)/sat-differential.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_k4/test_slot_boundary.py --result-out $(VERIFY_TMP)/slot-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_k4/verify_drat.py --hash-only

verify-audit:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_real/test_countcegar_real.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_real/validate_manifest.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/efx_chambers/verify_radii.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/efx_chambers/verify_radii_exact.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/multifloater_parking/verify_small.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) supplement/test_build_release.py

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
