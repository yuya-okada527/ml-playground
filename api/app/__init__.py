__version__ = '0.1.0'

import os
import sys
from pathlib import Path

__version__ = '0.1.0'

app_path = os.path.join(
    Path(__file__).resolve().parents[1],
    "app"
)

sys.path.append(app_path)
