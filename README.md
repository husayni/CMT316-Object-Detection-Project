# Applications of Machine Learning Project: Object Detection

This repository contains the code and resources for the Object Detection project.

---

## Repository Structure

```
.
├── Makefile                # Commands for managing the Conda environment
├── README.md               # This file
├── data/                   # Raw and processed data files
├── docs/                   # Project documentation
├── environment.yml         # Primary Conda environment definition
├── hello.py                # Example script
├── notebooks/              # Jupyter notebooks for analysis
│   └── 01_EDA.ipynb        # Exploratory Data Analysis
├── scripts/                # Utility scripts (e.g. data ingestion, data splitting)
└── src/                    # Application / library source code
```

---

## Development Setup

### Prerequisites

- **Conda** (Miniconda or Anaconda) installed.  
- GNU **make** (on Windows, use Git Bash, MSYS2/Cygwin, or WSL).  
- **Python 3.9+** (managed via Conda).

### 1. Create & Activate Environment

Use the provided `Makefile` to spin up your Conda environment from `environment.yml`:

```bash
# Create the environment
make create-env

# Activate it
conda activate objdet
```
### 2. Exporting Changes

After you add or update dependencies, regenerate `environment.yml`:

```bash
make export-env
```

### 3. Create .env file

Create a copy of `.env.sample` and rename it to `.env`.

---

## Working with the Code

- **`src/`**: core modules and library code. Organize by feature or package.
- **`scripts/`**: small utilities for ingestion, preprocessing, etc. Make them idempotent.
- **`notebooks/`**: exploratory analyses etc. Keep notebooks clean and ensure they run top-to-bottom.
  - **Naming Convention**: prefix filenames with a two-digit index and a concise description using snake_case, e.g., `01_EDA.ipynb`, `02_data_cleaning.ipynb`, `03_feature_engineering.ipynb`.

