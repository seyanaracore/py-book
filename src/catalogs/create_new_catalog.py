from constants import *
from src.catalogs.get_catalog_path import get_catalog_path


def create_catalog(name: str):
    catalog_path = get_catalog_path(name)

    data = CATALOG_COL_SEP.join([col for col in CATALOG_COLUMNS.values()])

    with open(catalog_path, 'w', encoding='utf-8') as file:
        file.write(data)
