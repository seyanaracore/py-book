from pathlib import Path

from constants import CATALOGS_FOLDER_PATH, CATALOG_FILE_EXT


def get_catalog_path(catalog_name: str):
    return Path(CATALOGS_FOLDER_PATH, f'{catalog_name}.{CATALOG_FILE_EXT}')
