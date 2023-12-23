import uuid

from common_types import CatalogInstance
from constants import MENU_EXIT_CODE, CATALOG_COLUMNS
from enums import ECatalogCol
from lib import custom_input
from src.catalogs.check_catalog_exist import check_catalog_exist
from src.catalogs.create_new_catalog import create_catalog
from src.catalogs.get_catalog import get_catalog, EGetCatalogCodes
from src.catalogs.get_catalogs_list import get_catalogs_list, CatalogList
from src.catalogs.print_catalog import print_catalog
from src.catalogs.print_catalogs_list import print_catalogs_list
from src.catalogs.remove_catalog import remove_catalog
from src.catalogs.write_catalog import write_catalog
from src.menu import EMenuList, show_menu, menu_list
from src.print_users import print_finded_users


def get_catalogs_list_handler() -> CatalogList | None:
    """
    Выведет список справочников или сообщение об их отсутствии. Вернет список при наличии
    """
    catalogs_list = get_catalogs_list()

    if catalogs_list:
        print_catalogs_list(catalogs_list)
    else:
        print('Пока нет ни одного справочника. Создай первый.')

    return catalogs_list


def create_catalog_handler():
    def validator(_new_catalog_name: str):
        if check_catalog_exist(_new_catalog_name):
            print(f'\nСправочник с именем \"{_new_catalog_name}\" уже существует.\n')
            return False
        return True

    new_catalog_name = custom_input.with_validate(f'Введи название для нового справочника.', validator)

    if new_catalog_name is MENU_EXIT_CODE:
        return

    create_catalog(new_catalog_name)

    print('\nСправочник успешно создан\n')


def get_catalog_handler(
        catalog_list=None,
        validate_catalog_len=True,
        text=f'Введите порядковый номер справочника.'
) -> CatalogInstance | None:
    if catalog_list is None:
        catalog_list = get_catalogs_list_handler()

    def validator(_catalog_num: str):
        try:
            var = catalog_list[int(_catalog_num) - 1]
            return True
        except (IndexError, ValueError):
            return False

    catalog_num = int(custom_input.with_validate(text, validator))

    if catalog_num is MENU_EXIT_CODE:
        return MENU_EXIT_CODE

    catalog_name = catalog_list[catalog_num - 1]['name']
    catalog = get_catalog(catalog_name, validate_catalog_len)

    if catalog is EGetCatalogCodes.catalog_is_empty:
        print(f'Справочник \"{catalog_name}\" пуст\n')
        return
    elif catalog is EGetCatalogCodes.catalog_not_exist:
        print(f'Справочника с таким названием \"{catalog_name}\" нет\n')
        return

    return catalog


def find_by_phone_handler():
    catalog = get_catalog_handler()

    if not catalog:
        return

    print_catalog(catalog)

    phone_num = custom_input.non_nullable('\nВведите номер телефона для поиска')

    if phone_num is MENU_EXIT_CODE:
        return

    catalog_keys = list(catalog['data'].keys())
    phone_col_name = CATALOG_COLUMNS[ECatalogCol.phone]

    phone_col_is_exist = phone_col_name in catalog_keys

    if not phone_col_is_exist:
        print('Не найдена колонка телефонов в справочнике')
        return

    phone_col = catalog['data'][phone_col_name]

    users_idx_list = [idx for idx, phone in enumerate(phone_col) if phone == phone_num]

    if not users_idx_list:
        print('\nЧеловек с таким телефоном не найден.\n')
        return

    print_finded_users(catalog, users_idx_list)


def change_number_handler():
    catalog = get_catalog_handler()

    if catalog == MENU_EXIT_CODE:
        return

    print_catalog(catalog)

    def validator(row_idx: str):
        return row_idx.isdigit()

    record_idx = int(custom_input.with_validate(f'Введите порядковый номер записи для замены номера', validator))

    target_row_idx = record_idx - 1
    try:
        var = catalog['data']['id'][target_row_idx]
    except IndexError:
        print('Ошибка получения записи по данному номеру')
        return

    new_phone_num = custom_input.non_nullable(f'Введите новый номер телефона.')

    target_col: list = catalog['data'][CATALOG_COLUMNS[ECatalogCol.phone]]
    target_col[target_row_idx] = new_phone_num

    write_catalog(catalog)

    print('Телефон успешно обновлен')


def delete_record_handler():
    catalog = get_catalog_handler()

    if catalog == MENU_EXIT_CODE:
        return

    print_catalog(catalog)

    def validator(row_idx: str):
        return row_idx.isdigit()

    record_idx = int(custom_input.with_validate(f'Введите порядковый номер записи для удаления', validator))

    target_row_idx = record_idx - 1
    try:
        var = catalog['data']['id'][target_row_idx]
    except IndexError:
        print('Ошибка получения записи по данному номеру')
        return

    for col_name in catalog['data'].keys():
        del catalog['data'][col_name][target_row_idx]

    write_catalog(catalog)

    print('Запись успешно удалена')


def add_record_handler():
    catalog = get_catalog_handler(None, False)

    if catalog == MENU_EXIT_CODE:
        return

    cols_list = list(catalog['data'].keys())
    cols_list.remove(CATALOG_COLUMNS[ECatalogCol.id])

    for col in cols_list:
        print("")
        field_value = custom_input.non_nullable(f'Введите значение для поля \"{col}\"')

        if field_value is MENU_EXIT_CODE:
            return

        catalog['data'][col].append(field_value)

    catalog['data'][CATALOG_COLUMNS[ECatalogCol.id]].append(str(uuid.uuid4()))
    write_catalog(catalog)

    print('\nЗапись успешно создана\n')


def add_record_from_another_catalog_handler():
    catalogs_list = get_catalogs_list_handler()

    if not catalogs_list:
        return

    if len(catalogs_list) < 2:
        print('У тебя всего один справочник')

    print_catalogs_list(catalogs_list)
    source_catalog = get_catalog_handler(catalogs_list, True, 'Введите номер справочника откуда нужно перенести запись')

    if not source_catalog or source_catalog is MENU_EXIT_CODE:
        return

    print_catalog(source_catalog)

    def validator(row_idx: str):
        return row_idx.isdigit()

    record_idx = int(custom_input.with_validate(f'Введите порядковый номер записи для переноса', validator))

    target_row_idx = record_idx - 1
    try:
        var = source_catalog['data']['id'][target_row_idx]
    except IndexError:
        print('Ошибка получения записи по данному номеру')
        return

    catalogs_list = list(filter(lambda catalog: catalog['name'] != source_catalog['name'], catalogs_list))

    print_catalogs_list(catalogs_list)
    target_catalog = get_catalog_handler(catalogs_list, False, 'Введите номер справочника куда нужно перенести запись')

    if not target_catalog:
        return

    for col_name in source_catalog['data'].keys():
        if col_name in target_catalog['data']:
            target_catalog['data'][col_name].append(source_catalog['data'][col_name][target_row_idx])
        else:
            print(f'Колонка \"{col_name}\" не найдена в целевой таблице')

    for col_name in source_catalog['data'].keys():
        del source_catalog['data'][col_name][target_row_idx]

    write_catalog(source_catalog)
    write_catalog(target_catalog)

    print('\nЗапись успешно перенесена\n')


def remove_catalog_handler():
    catalogs_list = get_catalogs_list()

    if not catalogs_list:
        return

    def validator(catalog_idx: str):
        return catalog_idx.isdigit()

    print_catalogs_list(catalogs_list)

    catalog_idx = int(custom_input.with_validate('Введите порядковый номер справочника для удаления', validator))

    if catalog_idx is MENU_EXIT_CODE:
        return

    is_removed = remove_catalog(catalogs_list[catalog_idx - 1]["path"])

    if is_removed:
        print('\nСправочник успешно удален\n')


def init():
    choice = None

    while choice != EMenuList.exit_menu:
        choice = show_menu(menu_list)

        match choice:
            case EMenuList.get_catalogs_list:
                get_catalogs_list_handler()

            case EMenuList.create_catalog:
                create_catalog_handler()

            case EMenuList.print_catalog:
                catalog = get_catalog_handler()

                if catalog:
                    print_catalog(catalog)

            case EMenuList.find_by_phone:
                find_by_phone_handler()

            case EMenuList.add_record:
                add_record_handler()

            case EMenuList.change_phone:
                change_number_handler()

            case EMenuList.delete_record:
                delete_record_handler()

            case EMenuList.remove_catalog:
                remove_catalog_handler()

            case EMenuList.add_record_from_another_catalog:
                add_record_from_another_catalog_handler()

            case EMenuList.incorrect_input:
                print('Некорректный ввод')


init()
