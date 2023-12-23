import os
from os import listdir
from os.path import isfile
from pathlib import Path
from typing import TypedDict

from constants import CATALOGS_FOLDER_PATH, CATALOG_FILE_EXT


class CatalogListItem(TypedDict):
    name: str
    path: Path


type CatalogList = list[CatalogListItem]


def get_catalogs_list() -> CatalogList | None:
    folder_path = Path(CATALOGS_FOLDER_PATH)

    catalogs_list = [
        CatalogListItem(name=os.path.splitext(file_name)[0], path=Path(folder_path, file_name))
        for file_name in listdir(folder_path)
        if isfile(Path(folder_path, file_name)) and Path(folder_path, file_name).suffix == f'.{CATALOG_FILE_EXT}'
    ]

    return catalogs_list if len(catalogs_list) > 0 else None
