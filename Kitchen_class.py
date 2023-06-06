import time
from threading import Thread
import Orders
import restaurant_runner_class
import Menu_class


class DynamicQueue:
    """ Псевдо очередь с приоритетом"""

    d_queue = []  # хранит [приоритет, имя, количество, номера столов]

    def insert(self, item: list[int, str, int, [int]]):
        """
        Не производит перекомпановку, но приоритеты учитываются при вставке нового объекта.
        Также производится повышение приоритета объектов, перед которыми
        был вставлен новый объект
        """

        for idx in range(len(self.d_queue)):
            if self.d_queue[idx][1] == item[1]:
                self.d_queue[idx][2] += item[2]
                self.d_queue[idx][3] += item[3]
                return
            if self.d_queue[idx][0] > item[0]:
                self.d_queue.insert(idx, item)
                for i in range(idx + 1, len(self.d_queue)):
                    self.d_queue[i][0] += 1
                return
        self.d_queue.append(item)

    def pop(self, idx: int) -> list[str, int, list[str]]:
        return self.d_queue.pop(idx)[1:]

    @property
    def len(self):
        return len(self.d_queue)


class DishPerformer:
    """
    Класс - производящая единица, осуществляющая зависящую от реального времени
    готовку блюд в соответствии со специализациями

    """

    cur_dish = []  # [название, количество, список столов, время готовки одной порции]
    start_time = 0  # Время на чала готовки

    def __init__(self, ready_dishes_list: list,
                 specializations: list[str],
                 name):
        self.ready_dishes = ready_dishes_list
        self.specializations = specializations
        self.name = name

    def set_task(self, tasks_queue: DynamicQueue, menu: Menu_class.Menu):
        """
        Функция отвечает за получение задания из очереди, в соотвецтвии со
        своими специализациями

        :arg
            tasks_queue - экземпляр DynamicQueue, в котором хранятся текущие задачи по готовке
            menu - экземпляр класса Menu, в котором указаны время готовки.
        """
        # DynamicQueue : [приоритет, имя, количество, заказчики]
        idx = 0
        while not self.cur_dish and idx < tasks_queue.len:
            if menu.menu_storage[tasks_queue.d_queue[idx][1]][1] in self.specializations:
                set_time = menu.menu_storage[tasks_queue.d_queue[idx][1]][3]
                self.cur_dish = tasks_queue.pop(idx) + [set_time]
                self.start_time = time.time()
                return
            idx += 1

    def tick(self):
        """ Функция осуществляет проверку на истечение времени на готовку"""

        if self.cur_dish:
            if time.time() - self.start_time >= self.cur_dish[3] + (self.cur_dish[1] - 1):
                self.ready_dishes.append([self.cur_dish[0], self.cur_dish[2]])
                self.cur_dish.clear()

    def get_info(self):
        print(self.name)
        print('Специализации :', *self.specializations)
        print('Задание :', *self.cur_dish)

    @property
    def is_empty(self):
        return not bool(self.cur_dish)


class CookingTerminal:
    tasks_queue = DynamicQueue()
    specializations_set = set()
    __performers_list = []
    ready_dishes = []  # :[Название, список столиков]
    runner = restaurant_runner_class.RestaurantRunner()

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(CookingTerminal, cls).__new__(cls)
            cls.runner.connect_cooking_terminal(cls._instance)
        return cls._instance

    def set_menu(self, menu: Menu_class.Menu):
        if len(menu.dishes()) != 0:
            self._cur_menu = menu
            self.check_menu()
        else:
            print('Данное меню пустое. Подключение не осуществилось.')

    def check_menu(self):
        """ Проверяет отметки о доступности блюд в меню в соответствии с доступными терминалу специализациями"""

        if not hasattr(self, '_cur_menu'):
            return
        for name in self._cur_menu.menu_storage.keys():
            if self._cur_menu.menu_storage[name][1] not in self.specializations_set:
                self._cur_menu.menu_storage[name][2] = False

    def add_performer(self, specializations: list[str], name='executor'):
        self.__performers_list.append(DishPerformer(self.ready_dishes, specializations, name))
        for specialization in specializations:
            self.specializations_set.add(specialization)
        self.check_menu()

    def remove_performer(self, performer_name: str):
        for performer in self.__performers_list:
            if performer.name == performer_name:
                self.__performers_list.remove(performer)

    def tick(self):
        """
        Отвечает за исполнение методов tick() у всех DishPerformer,
        прикреплённых к данному терминалу и проверку их бездействия

        """

        if not hasattr(self, '_cur_menu'):
            print('К кухне ещё не подключено меню')
            return
        for performer in self.__performers_list:
            if performer.is_empty:
                performer.set_task(self.tasks_queue, self._cur_menu)
            performer.tick()
        if self.ready_dishes:
            self.runner.send_ready_dishes(self.ready_dishes)
            self.ready_dishes.clear()

    def add_tasks(self, order: Orders.Order):
        """
        Выделяет нужные кухни задания из экземпляра Order и отправляет их
        соответственно в очередь

        """

        if not hasattr(self, '_cur_menu'):
            print('К кухне ещё не подключено меню')
            return
        for dish, data in order.dishes_list.items():
            if data[0] > 0:
                order.dishes_list[dish][3] += order.dishes_list[dish][0]
                self.tasks_queue.insert([
                                        self._cur_menu.menu_storage[dish][3],  # приоритет = время готовки
                                        dish,                                  # название блюда
                                        data[0],                               # количество
                                        [order.table_num]                      # номер стола
                                        ])
                order.dishes_list[dish][0] = 0

    def get_info(self):
        for per in self.__performers_list:
            per.get_info()
        print('Очередь: ', self.tasks_queue.d_queue)
        print(self.ready_dishes)

    def open_menu(self):
        """ Меню управления некоторыми методами кухни """

        if not hasattr(self, '_cur_menu'):
            print('К кухне ещё не подключено меню')
            return
        while True:
            print("______ Меню терминала кухни ______")
            print(self._cur_menu)
            print('Опции:\n'
                  '  ban {имя блюда} - запретить для заказа\n'
                  '  allow {имя блюда} - разрешить для заказа\n'
                  '  info - получить информацию\n'
                  '  close - выйти из меню')

            command = list(input().rstrip().split())

            if len(command) == 2:
                if command[0] == 'ban':
                    self._cur_menu.ban_dish(command[1])
                elif command[0] == 'open':
                    self._cur_menu.allow_dish(command[1])
                else:
                    print('Неверная команда')
            elif command[0] == 'info':
                self.get_info()
            elif command[0] == 'close':
                return
            else:
                print('Неизвестная команда')
