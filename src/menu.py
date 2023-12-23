import enum

from constants import MENU_EXIT_CODE


class EMenuList(enum.Enum):
    get_catalogs_list = 'GET_CATALOGS_LIST'
    get_catalog = 'GET_CATALOG'
    print_catalog = 'PRINT_CATALOG'
    find_phone_by_surname = 'FIND_PHONE_BY_SURNAME'
    change_phone = 'CHANGE_PHONE'
    delete_record = 'DELETE_RECORD'
    find_by_phone = 'FIND_BY_PHONE'
    create_catalog = 'CREATE_CATALOG'
    add_record = 'ADD_RECORD'
    add_record_from_another_catalog = 'ADD_RECORD_FROM_ANOTHER_CATALOG'
    incorrect_input = 'INCORRECT_INPUT'
    remove_catalog = 'REMOVE_CATALOG'
    exit_menu = MENU_EXIT_CODE


type IMenuList = list[dict[str, str]]

menu_list: IMenuList = [
    {'code': EMenuList.get_catalogs_list, 'text': 'Посмотреть справочники'},
    {'code': EMenuList.create_catalog, 'text': 'Создать справочник'},
    {'code': EMenuList.print_catalog, 'text': 'Распечатать справочник'},
    {'code': EMenuList.change_phone, 'text': 'Изменить номер телефона'},
    {'code': EMenuList.find_by_phone, 'text': 'Найти абонента по номеру телефона'},
    {'code': EMenuList.add_record_from_another_catalog, 'text': 'Добавить абонента из другого справочника'},
    {'code': EMenuList.add_record, 'text': 'Добавить абонента в справочник'},
    {'code': EMenuList.remove_catalog, 'text': 'Удалить справочник'},
    {'code': EMenuList.delete_record, 'text': 'Удалить запись'},
]

menu_exit_item = f'{MENU_EXIT_CODE}. Закончить работу'


def show_menu(menu: IMenuList) -> EMenuList:
    numbered_menu = [f'{idx + 1}. {menu_item.get('text')}' for idx, menu_item in enumerate(menu)]
    numbered_menu.append(menu_exit_item)

    print("\n".join(numbered_menu))

    choice = input('\nВыбор: ')

    if not choice.isdigit():
        return EMenuList.incorrect_input
    else:
        choice = int(choice)

    return EMenuList.exit_menu if choice is int(MENU_EXIT_CODE) else menu[choice - 1].get('code')
