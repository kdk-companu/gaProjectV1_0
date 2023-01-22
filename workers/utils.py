project_menus = {
    1: {'name': 'Пользователи', 'access': '1',
        'menu_up': [{'title_up': 'Сертификаты', 'icon_up': 'nav-icon fas fa-file', 'url_up': 'workers_certificates'},
                    {'title_up': 'Сотрудники', 'icon_up': 'nav-icon fas fa-user-circle', 'url_up': 'workers'},
                    # {'title_up': 'Оборудование', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'workers'},
                    # {'title_up': 'Квалификации', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'workers'},
                    # {'title_up': 'СИЗ', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'workers'},
                    # {'title_up': 'Табеля', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'workers'}
                    ]
        },
    2: {'name': 'Проекты', 'access': '1',
        'menu_up': [
            {'title_up': 'Задания на разработку', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'development_task'},
            # {'title_up': 'Заводские испытания', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'development_task'},
            # {'title_up': 'Ожидание наладки', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'development_task'},
            # {'title_up': 'Пусконаладка', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'development_task'},
            # {'title_up': 'Опытная эксплуатация', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'development_task'},
            # {'title_up': 'Законченные проекты', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'development_task'}
        ]
        },
    # 3: {'name': 'Документация', 'access': '1',
    #     'menu_up': [
    #         {'title_up': 'Тех. требования', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'base_page', 'menu_down': [
    #             {'title_down': 'Бованенкого', 'icon_down': 'nav-icon fas fa-chart-pie', 'url_down': 'base_page'},
    #             {'title_down': 'Чаянда', 'icon_down': 'far fa-circle nav-icon', 'url_down': 'base_page'}]},
    #         {'title_up': 'Разработка', 'icon_up': 'far fa-circle nav-icon', 'url_up': 'base_page',
    #          'menu_down': [
    #              {'title_down': 'Бованенкого', 'icon_down': 'nav-icon fas fa-chart-pie', 'url_down': 'base_page'},
    #              {'title_down': 'Чаянда', 'icon_down': 'nav-icon fas fa-chart-pie', 'url_down': 'base_page'}]}]
    #     },
    4: {'name': 'Настройки', 'access': '1',
        'menu_up': [
            {'title_up': 'Пользователи', 'icon_up': 'nav-icon fas fa-suitcase', 'url_up': '', 'menu_down': [
            {'title_down': 'Управление/Подразделение', 'icon_down': 'far fa-circle nav-icon',
             'url_down': 'subdivision', 'permission': 'workers.view_subdivision'},
            {'title_down': 'Отделы', 'icon_down': 'far fa-circle nav-icon', 'url_down': 'department',
             'permission': 'workers.view_department'},
            {'title_down': 'Должности', 'icon_down': 'far fa-circle nav-icon', 'url_down': 'chief',
             'permission': 'workers.view_chief'}
        ]},
    #         {'title_up': 'Проекты', 'icon_up': 'far fa-circle nav-icon', 'url_up': 'base_page',
    #          'menu_down': [
    #              {'title_down': 'Фирмы', 'icon_down': 'nav-icon fas fa-chart-pie', 'url_down': 'organization'},
    #              {'title_down': 'Сертификаты части', 'icon_down': 'nav-icon fas fa-chart-pie', 'url_down': 'base_page'}]},
                #
                #
                # {'title_up': 'Проекты', 'icon_up': 'nav-icon fas fa-book', 'url_up': 'base_page'}
        ]
       }
}


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['project_menus'] = project_menus
        return context
