ENV_FILE    ?= environment.yml
CONDA       ?= conda

.PHONY: help create-env export-env remove

help:
	@echo "Makefile targets:"
	@echo "  make create-env   - Create conda env from $(ENV_FILE)"
	@echo "  make export-env   - Export environment.yml (no prefix, no builds)"

create-env:
	$(CONDA) env create -f $(ENV_FILE)

export-env:
ifeq ($(OS),Windows_NT)
	@echo "Using Windows fallback for stripping prefix..."
	$(CONDA) env export --no-builds | findstr /V "^prefix:" > $(ENV_FILE)
else
	$(CONDA) env export --no-builds | sed '/^prefix:/d' > $(ENV_FILE)
endif