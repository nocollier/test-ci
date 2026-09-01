"""
Execute files passed in as arguments if they follow a `data/*.py` pattern.
To run the script on all files that have changed since the tip of main:

python run_generation_scripts.py $(git diff --name-only HEAD main)
"""

import subprocess
import sys
from pathlib import Path

from loguru import logger


def execute_script(filename: Path) -> list[Path]:
    """
    Execute the script and return the generated dataset(s).

    Note
    ----
    We assume that the user script will generate datasets to ingest
    in the parent directory of the script and these will be the only
    netCDF files found in this directory.
    """
    logger.info(f"Executing {filename=}...")
    res = subprocess.run(
        ["uv", "run", "python", str(filename.name)],
        cwd=str(filename.parent),
        check=True,
        capture_output=True,
    )
    # Log stdout and stderr
    for line in res.stdout.decode("utf-8").strip().split("\n"):
        logger.info(str(line).strip())
    for line in res.stderr.decode("utf-8").strip().split("\n"):
        logger.debug(str(line).strip())
    return [f for f in filename.parent.glob("*.nc")]


if __name__ == "__main__":
    scripts_to_run = [
        Path(f) for f in sys.argv[1:] if f.startswith("data") and f.endswith(".py")
    ]
    if not scripts_to_run:
        logger.info(f"We didn't find anything to run: {sys.argv[1:]=}")
        sys.exit(0)
    logger.info(f"Found {scripts_to_run=}")

    # execute each script
    generated_datasets: list[Path] = []
    for script in scripts_to_run:
        generated_datasets += execute_script(script)

    # save a text file with each dataset to check/ingest
    with open("to_ingest.txt", "w") as fout:
        _ = fout.write("\n".join([str(f) for f in generated_datasets]))
