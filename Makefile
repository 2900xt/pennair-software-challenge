# PennAir 2024 shape detection -- common tasks.
# Run `make` or `make help` for the list.

VENV    := .venv
PY      := $(VENV)/bin/python
PYTEST  := $(VENV)/bin/pytest
STATIC  := PennAir 2024 App Static.png
DYNAMIC := PennAir 2024 App Dynamic.mp4
HARD    := PennAir 2024 App Dynamic Hard.mp4

.DEFAULT_GOAL := help
.PHONY: help setup demo stages video video-hard test clean distclean

help:  ## show this help
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

setup:  ## create .venv and install the package (run this first)
	python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --upgrade pip
	$(PY) -m pip install --quiet -e ".[dev]"
	@echo "ready -- now run: make demo"

demo: | $(VENV)  ## Part 1: detect shapes in the static image
	$(PY) -m pennair image "$(STATIC)"

stages: | $(VENV)  ## Part 1 + a contact sheet of every pipeline stage
	$(PY) -m pennair image "$(STATIC)" --stages

video: | $(VENV)  ## Part 2: live viewer on the dynamic video
	$(PY) -m pennair video "$(DYNAMIC)"

video-hard: | $(VENV)  ## Part 2 + 3: live viewer on the hard video
	$(PY) -m pennair video "$(HARD)"

test: | $(VENV)  ## run the test suite
	$(PYTEST) -q

clean:  ## remove generated output and caches
	rm -rf out .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +

distclean: clean  ## also remove the virtualenv
	rm -rf $(VENV) *.egg-info

$(VENV):
	@echo "no virtualenv found -- run 'make setup' first" >&2; exit 1
