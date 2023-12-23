from common_types import CatalogInstance
from utils.transform_catalog import transform_catalog_to_list


def print_catalog(catalog: CatalogInstance):
    to_print = transform_catalog_to_list(catalog)
    with_num = []

    for (idx, row) in enumerate(to_print):
        row.insert(0, '#' if idx == 0 else str(idx))
        with_num.append(row)

    print("")
    for row in with_num:
        print('| {:3} | {:15} | {:15} | {:15} | {:25} | {:25} '.format(*row))

    print("")
