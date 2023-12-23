from os.path import isfile

from src.catalogs.get_catalog_path import get_catalog_path


def check_catalog_exist(catalog_name: str):
    catalog_path = get_catalog_path(catalog_name)

    return isfile(catalog_path)
