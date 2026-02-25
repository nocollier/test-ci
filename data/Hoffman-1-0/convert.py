from pathlib import Path

import requests

# Some fake work, let's assume here that downloading the raw data IS formatting it too.
remote_source = "https://www.ilamb.org/ILAMB-Data/DATA/nbp/HOFFMAN/nbp_1850-2010.nc"
resp = requests.get(remote_source, stream=True)
resp.raise_for_status()

CHUNKSIZE = 2**20
local_source = Path("nbp_1850-2010.nc")
if local_source.is_file():
    print(f"Already have downloaded {local_source=}")
with open(local_source, "wb") as fdl:
    for chunk in resp.iter_content(chunk_size=CHUNKSIZE):
        if chunk:
            fdl.write(chunk)
