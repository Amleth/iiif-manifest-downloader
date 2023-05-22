import argparse
import os
from pathlib import Path
import requests
import time

parser = argparse.ArgumentParser()
parser.add_argument('--manifest')
args = parser.parse_args()

manifest = requests.get(args.manifest).json()

folder = manifest["@id"].replace("/", "_")
try:
    os.mkdir(folder)
except FileExistsError:
    pass

i = 0
for canvas in manifest["sequences"][0]['canvases']:
    image = canvas["images"][0]["resource"]["@id"]
    print(image)

    r = requests.get(image)

    while r.status_code == 429:
        time.sleep(2)
        r = requests.get(image)

    with open(Path(folder, str(i) + "." + image.split(".")[-1]), "wb") as f:
        f.write(r.content)

    i += 1
