PYTHON ?= python3
TECTONIC ?= tectonic
CAIRO_LIB_DIR ?=

.PHONY: all figures check clean

all: figures
	$(TECTONIC) proof.tex

figures:
	$(PYTHON) scripts/make_figures.py
	$(if $(CAIRO_LIB_DIR),DYLD_FALLBACK_LIBRARY_PATH="$(CAIRO_LIB_DIR)") $(PYTHON) scripts/export_figures.py

check:
	$(PYTHON) scripts/check_math.py

clean:
	rm -f proof.aux proof.log proof.out proof.xdv proof.fls proof.fdb_latexmk
