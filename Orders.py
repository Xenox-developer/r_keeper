from Menu_class import Menu
import restaurant_runner_class
from data_base import Bill, SalesDatabase
from typing import Optional
from datetime import date


class Order:
    __order_id = -1
    table_num = 0

    def __init__(self, order_id: int, table_num: int):
        self.__order_id = order_id
        self.table_num = table_num
        # [наименование] = [ количество в буфере, стоимость одного, количество завершённых, количество на кухне]
        self.dishes_list = {}

    def add_dish(self, name: str, count: int, cost: int):
        if name in self.dishes_list.keys():
            self.dishes_list[name][0] += count
        else:
            self.dishes_list[name] = [count, cost, 0, 0]

    def remove_dish(self, name: str, count='all'):
        if name not in self.dishes_list.keys():
            print(f'Блюда с названием {name} нет в заказе')
            return
        if count == 'all':
            if self.dishes_list[name][2] == 0 and self.dishes_list[name][3] == 0:
                self.dishes_list.pop(name)
            else:
                self.dishes_list[name][0] = 0
        elif count.isdigit():
            if int(count) == self.dishes_list[name][0]:
                if self.dishes_list[name][2] == 0 and self.dishes_list[name][3] == 0:
                    self.dishes_list.pop(name)
                else:
                    self.dishes_list[name][0] = 0
            elif 0 <= int(count) < self.dishes_list[name][0]:
                self.dishes_list[name][0] -= int(count)
            else:
                print('Неверно указано количество')
        else:
            print('Неверно указано количество')

    def print(self):
        print('Номер стола', self.table_num)
        print('Заверенные:')
        for dish, data in self.dishes_list.items():
            if data[2] != 0:
                print(' ', dish, ':', f'{data[2]} * {data[1]} готовы')
            if data[3] != 0:
                print(' ', dish, ':', f'{data[3]} * {data[1]} готовятся')
        print('Буфер для отправления:')
        for dish, data in self.dishes_list.items():
            if data[0] != 0:
                print(' ', dish, ':', f'{data[0]}  * {data[1]}')

    def get_bill(self) -> Optional[Bill]:
        for item in self.dishes_list.items():
            if item[1][0] != 0 or item[1][3] !=0 :
                print('Заказ ещё не завершён')
                return
        print('Заказ завершён')
        total_summ = 0
        for item in self.dishes_list.items():
            print(f' {item[0]} : {item[2]} * {item[1]}')
            total_summ += item[1][1] * item[1][2]
        return Bill(self.__order_id, str(date.today()), self.dishes_list, total_summ)

    @property
    def get_id(self):
        return self.__order_id


class OrderTerminal:
    """ Общий терминал для управления заказами"""

    __orders_list = {}
    __next_id = 1
    __updated_status = set()
    runner = restaurant_runner_class.RestaurantRunner()

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(OrderTerminal, cls).__new__(cls)
            cls.runner.connect_orders_terminal(cls._instance)
        return cls._instance

    def set_menu(self, menu: Menu):
        if len(menu.dishes()) != 0:
            self._cur_menu = menu
        else:
            print('Данное меню пустое. Подключение не осуществилось.')

    def set_database(self, database: SalesDatabase):
        self.__database = database

    def add_dishes_to_order(self, cur_order: Order):
        self._cur_menu.print()
        print('Введите по очереди названия блюд "Название:количество" , завершение ввода "end"')

        input_str = input().rstrip()
        while input_str != 'end':
            dish_data = list(input_str.split(':'))
            if len(dish_data) == 2 and dish_data[1].isdigit():
                if dish_data[0] in self._cur_menu.dishes() and self._cur_menu.dish_available(dish_data[0]):
                    cur_order.add_dish(dish_data[0], int(dish_data[1]), self._cur_menu.get_price(dish_data[0]))
                else:
                    print('Данного блюда нет в меню')
            else:
                print('Неверный формат ввода блюда')
            input_str = input().rstrip()

    def remove_dishes_from_order(self, cur_order: Order):
        cur_order.print()
        print('Введите по очереди названия блюд "Название:количество" , завершение ввода "end"')

        input_str = input().rstrip()
        while input_str != 'end':
            dish_data = list(input_str.split(':'))
            if len(dish_data) == 2:
                cur_order.remove_dish(dish_data[0], dish_data[1])
            else:
                cur_order.remove_dish(dish_data[0])
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

    def send_order(self, cur_order: Order):
        """ Функция отправляет заказ через курьера на обработку на кухню"""

        self.runner.send_order_tasks(cur_order)

    def get_ready_dishes(self, ready_dishes: list[str, list[int]]):
        """ Функция для получения готовых блюд от курьера из кухни

            :arg
            ready_dishes - список пар (название блюда, номера столов для которых сделано)
        """

        for task in ready_dishes:
            for number in task[1]:
                self.__orders_list[number].dishes_list[task[0]][2] += self.__orders_list[number].dishes_list[task[0]][3]
                self.__orders_list[number].dishes_list[task[0]][3] = 0
                self.__updated_status.add(number)

    def open_menu(self):
        """ Меню управления добавлением заказов"""

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
                if table in self.__updated_status:
                    print('Стол -', table, ' !')
                else:
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
                print('Неизвестная команда')

    def open_order_menu(self, table_num: int):
        """Меню управления методами для работы с конкретным заказом"""

        if table_num not in self.__orders_list.keys():
            print('Заказа на этот стол нет!')
            return
        if table_num in self.__updated_status:
            self.__updated_status.remove(table_num)
        while True:
            print('______ Меню заказа для стола', table_num)
            print('Опции:\n'
                  '  add - Добавить блюда\n'
                  '  del - удалить блюда из заказа\n'
                  '  send - отправить буфер на кухню\n'
                  '  complete - завершить заказ и выслать чек\n'
                  '  update - обновить данные\n'
                  '  close - выйти из меню')
            print('Информация о заказе :')
            self.__orders_list[table_num].print()

            command = input().rstrip()

            if command == 'add':
                self.add_dishes_to_order(self.__orders_list[table_num])
            elif command == 'del':
                self.remove_dishes_from_order(self.__orders_list[table_num])
            elif command == 'send':
                self.send_order(self.__orders_list[table_num])
            elif command == 'update':
                pass
            elif command == 'complete':
                bill = self.__orders_list[table_num].get_bill()
                if bill:
                    self.__database.add_bill(bill)
                    self.__orders_list.pop(table_num)
                    return
            elif command == 'close':
                return
            else:
                print('Неизвестная команда')


