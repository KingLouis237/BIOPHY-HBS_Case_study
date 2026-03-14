# Setup For Beginners

This guide rewrites the README setup steps in slow motion. Assume nothing beyond a working laptop.

## 1. Install the prerequisites
1. **Python 3.11** – download from python.org if you do not already have it (`python --version` should print something like `3.11.7`).
2. **Git (optional)** – handy if you plan to pull updates. Skip it if you would rather download a ZIP.
3. **One environment manager** – either `uv` (fast, lightweight) or `conda`/`mamba` (full-featured). You can install both, but you only need one.

## 2. Get the repository files
### Option A: Git clone (recommended if you plan to contribute)
```bash
git clone https://github.com/<your-account>/hemoglobin-e6v-case-study.git
```
Git keeps the version history so you can pull future updates with `git pull`.

### Option B: Download ZIP (no Git required)
1. Visit the GitHub page and click **Code ? Download ZIP**.
2. Unzip the archive anywhere you like. It creates a folder such as `hemoglobin-e6v-case-study-main`.

## 3. Open a terminal inside the repo folder
Use `cd` to move into the folder you just created:
```bash
cd hemoglobin-e6v-case-study
```
Every command below assumes you are running it from this folder so relative paths like `scripts/sequence_summary.py` make sense.

## 4. Pick an environment strategy
### Option A: `uv` (reads `pyproject.toml`)
1. Install `uv` if needed (`pip install uv`).
2. From the repo root, run:
   ```bash
   uv sync
   ```
   What happens:
   - `uv` reads `pyproject.toml` (and `uv.lock` if it exists) to learn which packages and versions to install.
   - It creates a `.venv/` folder inside the repo and records a lockfile locally for reproducibility (Astral 2024).
   - You do **not** have to activate the environment manually; you will prefix commands with `uv run`.

### Option B: `conda` or `mamba` (reads `environment/environment.yml`)
1. Make sure Anaconda/Miniconda/Mambaforge is installed.
2. From the repo root, run:
   ```bash
   conda env create -f environment/environment.yml
   ```
   What happens:
   - Conda reads `environment/environment.yml`, sees the environment name (`hemoglobin-e6v`), the conda-forge channel, and every dependency (Python, Biopython, Matplotlib, NumPy, EMBOSS, BLAST+, pip extras).
   - It creates an isolated environment in your conda directory.
3. Activate it:
   ```bash
   conda activate hemoglobin-e6v
   ```
   Activation tells your shell to use the new interpreter and packages; without it, `python` would point to whatever happens to be installed globally.

### (Optional) Plain pip install for the CI smoke test
If you only want the exact packages used by the GitHub Actions smoke test, run:
```bash
python -m pip install -r requirements-smoke.txt
```
This installs Biopython, Matplotlib, and NumPy. You are responsible for BLAST+/EMBOSS binaries in this mode.

## 5. Run the smoke test
Regardless of the environment manager, the first command to run is the sequence summary:
- **uv workflow:**
  ```bash
  uv run python scripts/sequence_summary.py
  ```
- **conda/pip workflow:**
  ```bash
  python scripts/sequence_summary.py
  ```

Expected outputs:
- `data/processed/sequence_summary.tsv` – machine-readable table of record name, length, hydrophobicity, acidity/basicity ratio, source file.
- `reports/sequence_summary.md` – human-readable Markdown table with the same information.

Spot-check the table: the secret beta chain should have the same length as the canonical one but a slightly higher hydrophobic fraction because Val replaces Glu at position 6.

## 6. Continue with the workflow
Once the smoke test succeeds, follow `docs/06_runbook.md` for the complete command sequence. When you want to understand the logic behind each script, read `docs/03_pipeline_logic.md`. For the biological meaning of every metric, head to `docs/08_biological_interpretation.md` and `docs/09_results_and_discussion.md`.

## References
- Astral Software. 2024. "uv documentation." https://github.com/astral-sh/uv
- Anaconda, Inc. 2024. "Managing environments." https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-environments.html
