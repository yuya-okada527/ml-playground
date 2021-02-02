import os
from pathlib import Path


RESOURCES_PATH = os.path.join(
    Path(__file__).resolve().parents[2],
    "resources"
)


def get_resource(path: str, encoding="utf8"):
    with open(os.path.join(RESOURCES_PATH, path), encoding=encoding) as f:
        return f.read()
