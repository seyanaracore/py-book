from common_types import CatalogInstance

type CatalogRow = list[str]
type CatalogList = list[CatalogRow]


def transform_catalog_to_list(catalog: CatalogInstance):
    catalog_list: CatalogList = [list(catalog['data'].keys())]

    catalog_cols_names = catalog_list[0]
    first_col_name = catalog_cols_names[0]

    for row_idx, row in enumerate(catalog["data"][first_col_name]):
        catalog_list.append([])

        for col_name in catalog_cols_names:
            catalog_list[row_idx + 1].append(catalog['data'][col_name][row_idx])

    return catalog_list
