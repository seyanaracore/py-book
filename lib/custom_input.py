from typing import Callable

from constants import MENU_EXIT_CODE, INPUT_IS_ERROR

type ValidatorCb = Callable[[str], bool]


def non_nullable(text: str, add_exit_code=True) -> str:
    data = ''

    while data == '':
        data = input(f'{text}{'\n' + str(MENU_EXIT_CODE) + ' для возвращения.' if add_exit_code else ''}\n > ')

    return data


def with_validate(text: str, validator_cb: ValidatorCb, with_non_nullable=True, add_exit_code=True) -> str:
    input_data = INPUT_IS_ERROR

    while input_data is INPUT_IS_ERROR and input_data != MENU_EXIT_CODE:
        input_data = non_nullable(text, add_exit_code) if with_non_nullable else input(text)

        if input_data is MENU_EXIT_CODE:
            return input_data

        if not validator_cb(input_data):
            input_data = INPUT_IS_ERROR

    return input_data
