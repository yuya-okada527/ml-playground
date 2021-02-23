import os
from pathlib import Path

RESOURCES_PATH = os.path.join(
    Path(__file__).resolve().parents[2],
    "resources"
)


def get_resource(path: str, encoding: str = "utf8") -> str:
    with open(os.path.join(RESOURCES_PATH, path), encoding=encoding) as f:
        return f.read()
