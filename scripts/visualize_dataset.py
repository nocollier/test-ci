"""
Execute files passed in as arguments if they follow a `data/*.py` pattern.
To run the script on all files that have changed since the tip of main:

python run_generation_scripts.py $(git diff --name-only HEAD main)
"""

import sys
from pathlib import Path

import xarray as xr
from loguru import logger


def visualize(filename: Path) -> str:
    """ """
    logger.info(f"Executing {filename=}...")
    ds = xr.open_dataset(filename)
    return f"\n{ds}\n"


if __name__ == "__main__":
    datasets_to_visualize = [Path(f) for f in open(sys.argv[1], "r").readlines()]
    if not datasets_to_visualize:
        logger.debug(f"We didn't find anything to run: {sys.argv[1]=}")
        sys.exit(0)
    logger.info(f"Found {datasets_to_visualize=}")

    # visualize each dataset
    comment = """
## Dataset File Contents
```"""
    for dset in datasets_to_visualize:
        comment += visualize(dset)
    comment += "```"

    # save a text file with each dataset to check/ingest
    with open("ncdumps.txt", "w") as fout:
        _ = fout.write(comment)
