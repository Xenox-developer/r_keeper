import Kitchen_class
import Orders
import Menu_class
import data_base
import visitor_data
import Warehouse
from threading import Thread
import time


class RKeeper:

    __activity_indicator = False

    # Блок функций для блока заказа и обработки заказов блюд
    def __init__(self, orders_terminal: Orders.OrderTerminal, cooking_terminal: Kitchen_class.CookingTerminal,
                 sale_database: data_base.SalesDatabase, v_database: visitor_data.VisitorDatabase, 
                 w_database: Warehouse.WarehouseManager):
        self.__orders_terminal = orders_terminal
        self.__cooking_terminal = cooking_terminal
        self.__sale_database = sale_database
        self.__visitors_database = v_database
        self.__vs_menu = visitor_data.VisitorMenu(self.__visitors_database)
        self.__warehouse = w_database
        self.__w_menu = Warehouse.WarehouseMenu(self.__warehouse)
        self.__orders_terminal.set_database(sale_database, v_database)

    def add_dish_performers(self, specializations: list[str], name='executor'):
        self.__cooking_terminal.add_performer(specializations, name=name)

    def remove_dish_performer(self, performer_name: str):
        self.__cooking_terminal.remove_performer(performer_name)

    def set_restaurant_menu(self, menu:Menu_class.Menu):
        self.__orders_terminal.set_menu(menu)
        self.__cooking_terminal.set_menu(menu)


    def ping_cooking_terminal(self):
        while self.__activity_indicator:
            self.__cooking_terminal.tick()
            time.sleep(2)

    # Общий блок управления
    @property
    def indicator(self):
        return self.__activity_indicator

    def __open_global_menu(self):
        self.__activity_indicator = True
        while True:
            print("______ Меню системы R_Keeper ______")
            print('Опции:\n'
                  '  1 - Открыть меню Терминала кухни\n'
                  '  2 - Открыть меню терминала заказов\n'
                  '  3 - Открыть меню базы данных для продаж блюд\n'
                  '  4 - Открыть меню базы данных посетителей\n'
                  '  5 - Открыть меню базы данных склада\n'
                  '  close - выйти из меню')

            command = input().rstrip()

            if command == '1':
                self.__cooking_terminal.open_menu()
            elif command == '2':
                self.__orders_terminal.open_menu()
            elif command == '3':
                self.__sale_database.open_menu()
            elif command == '4':
                self.__vs_menu.open_menu()
            elif command == '5':
                self.__w_menu.open_menu()
            elif command == 'close':
                self.__activity_indicator = False
                return
            else:
                print('Неизвестная команда')

    def start(self):
        if not hasattr(self.__cooking_terminal, '_cur_menu'):
            print('Меню ещё не подключено. Начало работы невозможно')
            return
        self.__activity_indicator = True
        t1 = Thread(target=self.__open_global_menu)
        t2 = Thread(target=self.ping_cooking_terminal)

        t1.start()
        t2.start()
        t1.join()
        t2.join()


menu = Menu_class.Menu('menu_file.txt')
tem = Kitchen_class.CookingTerminal()
orders = Orders.OrderTerminal()
data = data_base.SalesDatabase('sales_data.txt')
vis_data = visitor_data.VisitorDatabase('visitors.txt')
warehouse_data = Warehouse.WarehouseManager('warehouse_products.txt')
main_class = RKeeper(orders, tem, data, vis_data, warehouse_data)
main_class.add_dish_performers(['Супы', 'Салаты', 'Закуски'], name='повар-1')
main_class.add_dish_performers(['Супы'], name='повар-2')
main_class.set_restaurant_menu(menu)
main_class.start()
