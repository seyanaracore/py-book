from common_types import CatalogInstance
from constants import CATALOG_COL_SEP
from utils.transform_catalog import transform_catalog_to_list


def write_catalog(catalog: CatalogInstance):
    catalog_list = transform_catalog_to_list(catalog)

    catalog_str = "\n".join([CATALOG_COL_SEP.join(catalog_row) for catalog_row in catalog_list])

    with open(catalog['path'], 'w', encoding='utf-8') as file:
        file.write(catalog_str)
