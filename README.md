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
├── scripts/                # Utility scripts (e.g. data ingestion, data splitting)
└── src/                    # Application / library source code
```

---

## Development Setup

### Prerequisites

- **Conda** (Miniconda or Anaconda) installed.  
    > to install conda on windows: 
    ```
    wget "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -outfile ".\Downloads\Miniconda3-latest-Windows-x86_64.exe"
    ```
    > Open The installer, make sure to check add to PATH option
- **make** (on Windows, use Git Bash, MSYS2/Cygwin, or WSL). 
    > to install make on windows Open Powershell with Administrator privileges and run: 
    ```
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor  3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```
    ```
    choco install make -y
    ```
    Verify the installation:
    ```
    make --version
    ```
- **Python 3.8+** (managed via Conda).
- **AWS Credentials** (Contact Hussain for it).

### Setup Development Environment

Use the provided `Makefile` to spin up Development Environment:

```bash
make setup

conda activate objdet
```
### Exporting Changes

if you add or update dependencies, regenerate `environment.yml`:

```bash
make export-env
```

### Create .env file

Create a copy of `.env.sample` and rename it to `.env`.

### Tracking New data with DVC

Example Scenario: You have a new data folder (data/preprocessed) that you want to track with DVC.

```bash
dvc add data/preprocessed
dvc push
git add data/preprocessed.dvc .gitignore
git commit -m "Track data/preprocessed with DVC"
```

---

## Working with the Code

- **`src/`**: core modules and library code. Organize by feature or package.
- **`scripts/`**: small utilities for ingestion, preprocessing, etc. Make them idempotent.
- **`notebooks/`**: exploratory analyses etc. Keep notebooks clean and ensure they run top-to-bottom.
  - **Naming Convention**: prefix filenames with a two-digit index and a concise description using snake_case, e.g., `01_EDA.ipynb`, `02_data_cleaning.ipynb`, `03_feature_engineering.ipynb`.

