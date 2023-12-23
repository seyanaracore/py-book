def print_catalogs_list(catalogs_list):
    print('\nСписок справочников:')

    for (idx, catalog) in enumerate(catalogs_list):
        print(f'{idx + 1}. {catalog.get('name')}')

    print('')
