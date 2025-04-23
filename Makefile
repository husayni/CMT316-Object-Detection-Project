ENV_FILE    ?= environment.yml
CONDA       ?= conda

.PHONY: help create-env export-env remove

help:
	@echo "Makefile targets:"
	@echo "  make create-env   		- Create conda env from $(ENV_FILE)"
	@echo "  make export-env   		- Export environment.yml (no prefix, no builds)"
	@echo "  make download-data		- Download data"
	@echo "  make setup        		- Create env and download data"

create-env:
	@echo "Creating conda env from $(ENV_FILE)..."
	$(CONDA) env create -f $(ENV_FILE)
	@echo "Environment created!"

export-env:
ifeq ($(OS),Windows_NT)
	@echo "Using Windows fallback for stripping prefix..."
	$(CONDA) env export --no-builds | findstr /V "^prefix:" > $(ENV_FILE)
else
	$(CONDA) env export --no-builds | sed '/^prefix:/d' > $(ENV_FILE)
endif

download-data:
	@echo "Downloading data..."
	conda run -n objdet dvc pull
	@echo "Data downloaded!"

setup : create-env download-data
