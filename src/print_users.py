from common_types import CatalogInstance
from src.catalogs.print_catalog import print_catalog


def print_finded_users(catalog: CatalogInstance, users_list_idx: [int]):
    res = CatalogInstance(name=catalog['name'], path=catalog['path'], data={})

    for col_name in list(catalog["data"].keys()):
        res["data"][col_name] = []

        for user_idx in users_list_idx:
            res["data"][col_name].append(catalog["data"][col_name][user_idx])

    print_catalog(res)
