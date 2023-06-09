
class Menu:
    """ Класс для хранения и управления данными о блюдах """

    menu_storage = {}  # [название блюда] = [стоимость, категория, наличие, время готовки (сек.)]

    def __init__(self, menu_file_name: str, availability=True):

        try:
            menu = open(menu_file_name, encoding='utf-8')
            cur_categories = ''
            for line in menu:
                line = line.rstrip()
                if line.find(':') == -1:
                    cur_categories = line
                else:
                    data = list(line.split(':'))
                    if len(data) >= 3:
                        self.menu_storage[data[0]] = [int(data[1]), cur_categories, availability, int(data[2])]
                    else:
                        print(f'Для блюда {data[0]} не хватает данных')
            menu.close()
        except FileNotFoundError:
            print('Не удалось найти файл меню')
        except ValueError:
            print('Цена и длительность готовки должны быть целочисленным значением')

    def __str__(self):
        string = ''
        for item in self.menu_storage.items():
            string += f'{item[0]} | {item[1][0]} | {item[1][1]} | {item[1][2]} | {item[1][3]} \n'
        return string

    def print(self):
        print('_____Меню_____')
        cur_categories = ''
        for dish in self.menu_storage.items():
            if dish[1][2]:
                if dish[1][1] != cur_categories:
                    cur_categories = dish[1][1]
                    print(cur_categories, ':')
                print(' ', dish[0], dish[1][0])

    def get_price(self, name: str):
        """ Получить цену по названию блюда"""

        return self.menu_storage[name][0]

    def dish_available(self, name: str):
        """Получить доступность блюда для заказа"""

        return self.menu_storage[name][2]

    def dishes(self):
        """ Получить список всех блюд """

        return self.menu_storage.keys()

    def ban_dish(self, dish_name: str):
        """ Запретить блюдо для заказа"""

        if dish_name in self.menu_storage.keys():
            self.menu_storage[dish_name][2] = False
        else:
            print('Данного блюда нет в меню')

    def allow_dish(self, dish_name: str):
        """ Разрешить блюдо для заказа"""

        if dish_name in self.menu_storage.keys():
            self.menu_storage[dish_name][2] = True
        else:
            print('Данного блюда нет в меню')

