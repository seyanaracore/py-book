import enum

from common_types import CatalogInstance
from constants import CATALOG_COL_SEP
from src.catalogs.check_catalog_exist import check_catalog_exist
from src.catalogs.get_catalog_path import get_catalog_path


class EGetCatalogCodes(enum.Enum):
    catalog_not_exist = 'catalog_not_exist'
    catalog_is_empty = 'catalog_not_exist'


def get_catalog(catalog_name: str, validate_catalog_len=True) -> CatalogInstance | EGetCatalogCodes:
    if not check_catalog_exist(catalog_name):
        return EGetCatalogCodes.catalog_not_exist

    catalog_path = get_catalog_path(catalog_name)
    res: CatalogInstance = CatalogInstance(name=catalog_name, path=catalog_path, data={})

    with open(catalog_path, 'r', encoding='utf-8') as file:
        data = file.read()
        splitted_data = data.split('\n')

        if validate_catalog_len and len(splitted_data) < 2:
            return EGetCatalogCodes.catalog_is_empty

        columns = splitted_data[0].split(CATALOG_COL_SEP)
        rows = splitted_data[1:len(splitted_data)]

        for column in columns:
            res['data'][column] = []

        for row in rows:
            row_data = row.split(CATALOG_COL_SEP)

            for (idx, row_col_data) in enumerate(row_data):
                res['data'][columns[idx]].append(row_col_data)

        return res
