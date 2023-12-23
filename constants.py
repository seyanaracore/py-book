from enums import ECatalogCol

CATALOGS_FOLDER_PATH = 'catalogs'
CATALOG_FILE_EXT = 'csv'

CATALOG_COLUMNS = {
    ECatalogCol.name: 'Имя',
    ECatalogCol.sur_name: 'Фамилия',
    ECatalogCol.phone: 'Телефон',
    ECatalogCol.description: 'Описание',
    ECatalogCol.id: 'id',
}
CATALOG_COL_SEP = ','

MENU_EXIT_CODE = '0'
INPUT_IS_ERROR = 'input_is_error'
