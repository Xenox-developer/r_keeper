from Menu_class import Menu


class Order:
    __total_summ = 0
    __order_id = -1
    __dishes_list = {}# [наименование] = [количество, стоимость одного]
    table_num = 0

    def __init__(self, order_id: int, table_num: int):
        self.__order_id = order_id
        self.table_num = table_num

    def add_dish(self, name: str, count: int, cost: int):
        if name in self.__dishes_list.keys():
            self.__dishes_list[name][0] += count
        else:
            self.__dishes_list[name] = [count, cost]
        self.__total_summ += count * cost

    def remove_dish(self, name: str, count='all'):
        if name not in self.__dishes_list.keys():
            print(f'Блюда с названием {name} нет в заказе')
            return
        if count == 'all':
            self.__total_summ -= self.__dishes_list[name][0] * self.__dishes_list[name][1]
            self.__dishes_list.pop(name)
        elif count.isdigit():
            if int(count) == self.__dishes_list[name][0]:
                self.__total_summ -= self.__dishes_list[name][0] * self.__dishes_list[name][1]
                self.__dishes_list.pop(name)
            elif 0 < int(count) < self.__dishes_list[name][0]:
                self.__dishes_list[name][0] -= int(count)
                self.__total_summ -= int(count) * self.__dishes_list[name][1]
            else:
                print('Неверно указано количество')
        else:
            print('Неверно указано количество')

    def print(self):
        print('Номер стола', self.table_num)
        for dish, data in self.__dishes_list.items():
            print(dish, ':', f'{data[0]} * {data[1]}')
        print(f'Total summ: {self.__total_summ}')

    @property
    def get_id(self):
        return self.__order_id


class OrderTerminal:
    __orders_list = {}
    __next_id = 1

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(OrderTerminal, cls).__new__(cls)
        return cls._instance

    def set_menu(self, menu: Menu):
        self._cur_menu = menu

    def add_dishes_to_order(self, cur_order: Order):
        self._cur_menu.print()
        print('Введите по очереди названия блюд "Название:количество" , завершение ввода "end"')

        input_str = input().rstrip()
        while input_str != 'end':
            dish_data = list(input_str.split(':'))
            if len(dish_data) == 2 and dish_data[0] in self._cur_menu.dishes() and dish_data[1].isdigit():
                    cur_order.add_dish(dish_data[0], int(dish_data[1]), self._cur_menu.get_price(dish_data[0]))
            input_str = input().rstrip()

    def create_order(self, table_num: int):
        if not hasattr(self, '_cur_menu'):
            print('Меню ещё не создано')
            return

        if table_num in self.__orders_list.keys():
            print('Данный стол уже занят , пожалуйста не нарушайте политику заведения')
            return

        self.__orders_list[table_num] = Order(self.__next_id, table_num)
        self.__next_id += 1

    def open_menu(self):
        while True:
            print("______ Меню терминала заказов ______")
            print('Опции:\n'
                  '  add {номер стола}- Добавить заказ\n'
                  '  open {номер стола в заказе} - войти в меню данного заказа\n'
                  '  close - выйти из меню')
            print('Текущие заказы :')
            if len(self.__orders_list.keys()) == 0:
                print('--')
            for table in self.__orders_list.keys():
                print('Стол -', table)

            command = list(input().rstrip().split())

            if len(command) == 2:
                if command[0] == 'add' and command[1].isdigit():
                    self.create_order(int(command[1]))
                elif command[0] == 'open' and command[1].isdigit():
                    self.open_order_menu(int(command[1]))
                else:
                    print('Неверная команда')
            elif command[0] == 'close':
                return
            else:
                print('Неверная команда')

    def open_order_menu(self, table_num: int):
        if table_num not in self.__orders_list.keys():
            print('Заказа на этот стол нет!')
            return
        while True:
            print('______ Меню заказа для стола', table_num)
            print('Опции:\n'
                  '  add - Добавить блюда\n'
                  '  del - удалить блюда из заказа\n'
                  '  complete - завершить заказ и выслать чек\n'
                  '  close - выйти из меню')
            print('Информация о заказе :')
            self.__orders_list[table_num].print()

            command = input()

            if command == 'add':
                self.add_dishes_to_order(self.__orders_list[table_num])
            elif command[0] == 'del':
                pass
                #self.remove_dishes_from_order()
            elif command == 'complete':
                pass
            elif command == 'close':
                return
            else:
                print('Неверная команда')



a = Menu('menu_file.txt')
b = OrderTerminal()
b.set_menu(a)
#b.open_menu()


