import os
from pathlib import Path

from common_types import CatalogInstance


def remove_catalog(target: CatalogInstance | Path):
    target_path = target['path'] if target is CatalogInstance else target

    if not target_path:
        return

    os.remove(target_path)
    return True
