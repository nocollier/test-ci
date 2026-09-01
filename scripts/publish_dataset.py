""" """

import hashlib
import sys
from pathlib import Path

from loguru import logger

if __name__ == "__main__":
    # do we have datasets to publish?
    datasets_to_publish = [Path(f) for f in open(sys.argv[1], "r").readlines()]
    if not datasets_to_publish:
        logger.debug(f"We didn't find anything to publish: {sys.argv[1]=}")
        sys.exit(1)
    logger.info(f"Found {datasets_to_publish=}")

    # read our current registry
    reg = {}
    with open("registry/data.txt") as fin:
        reg = {line.split()[0]: line.split()[1] for line in fin.readlines()}

    for dset in datasets_to_publish:
        key = str(dset).replace("data/", "")
        hash = hashlib.sha1(dset.read_bytes()).hexdigest()
        logger.info(f"{key=} {hash=}")
        if key in reg:
            if hash != reg[key].replace("sha1:", ""):
                logger.info(f"{key=} exists in the registry, this is an update.")
            else:
                logger.info(f"{key=} key exists and hash already matches.")
        else:
            logger.info(f"{key=} is new and being added to the registry.")
            reg[key] = f"sha1:{hash}"

    with open("registry/data.txt", "w") as fout:
        for key in sorted(reg):
            _ = fout.write(f"{key} {reg[key]}\n")
