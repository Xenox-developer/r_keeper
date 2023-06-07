from dataclasses import dataclass


@dataclass
class Visitor:
    phone_number: str
    first_name: str
    last_name: str


class VisitorDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.customers = []  # Список для хранения объектов Visitor
        self.loyalty_points = {}  # Словарь для хранения баллов лояльности
        self.registration_info = {}  # Словарь для хранения информации о регистрации
        self.discount_info = {}  # Словарь для хранения информации о скидках
        self.load_data()  # Загрузка данных из файла при создании экземпляра класса

    def add_visitor(self, phone_number: str, first_name: str, last_name: str):
        visitor = Visitor(phone_number, first_name, last_name)  # Создание объекта Visitor
        self.customers.append(visitor)  # Добавление посетителя в список
        self.save_data()  # Сохранение данных в файл

    def remove_visitor(self, phone_number: str):
        # Удаление посетителя из списка на основе номера телефона
        self.customers = [visitor for visitor in self.customers if visitor.phone_number != phone_number]
        self.save_data()  # Сохранение данных в файл

    def get_visitor_info(self, phone_number: str) -> Visitor:
        # Получение информации о посетителе на основе номера телефона
        for visitor in self.customers:
            if visitor.phone_number == phone_number:
                return visitor
        return None
    
    def get_loyalty_points(self, phone_number: str) -> int:
        # Получение количества баллов лояльности по номеру телефона
        if phone_number in self.loyalty_points:
            return self.loyalty_points[phone_number]
        return -1

    def increase_loyalty_points(self, phone_number: str, points: int):
        # Увеличение баллов лояльности у посетителя на основе номера телефона
        if phone_number in self.loyalty_points:
            self.loyalty_points[phone_number] += points
        else:
            self.loyalty_points[phone_number] = points
        self.save_data()  # Сохранение данных в файл

    def use_loyalty_points(self, phone_number: str, points: int) -> bool:
        # Использование баллов лояльности для предоставления скидки
        if phone_number in self.loyalty_points and self.loyalty_points[phone_number] >= points:
            self.loyalty_points[phone_number] -= points
            self.save_data()  # Сохранение данных в файл
            return True
        return False

    def add_discount(self, phone_number: str, discount_info: dict):
        # Добавление информации о скидке для посетителя на основе номера телефона
        self.discount_info[phone_number] = discount_info
        self.save_data()  # Сохранение данных в файл

    def check_discount_validity(self, phone_number: str) -> bool:
        # Проверка действительности скидки для посетителя на основе номера телефона
        return phone_number in self.discount_info

    def save_data(self):
        # Сохранение данных в файл
        with open(self.db_file, 'w') as f:
            f.write("Customers:\n")
            for visitor in self.customers:
                f.write(f"{visitor.phone_number},{visitor.first_name},{visitor.last_name}\n")
            f.write("Loyalty Points:\n")
            for phone_number, points in self.loyalty_points.items():
                f.write(f"{phone_number},{points}\n")
            f.write("Discount Info:\n")
            for phone_number, discount_info in self.discount_info.items():
                f.write(f"{phone_number},{discount_info}\n")

    def load_data(self):
        # Загрузка данных из файла
        self.customers = []  # Очистка списка посетителей
        self.loyalty_points = {}  # Очистка словаря баллов лояльности
        self.discount_info = {}  # Очистка словаря информации о скидках
        with open(self.db_file, 'r') as f:
            current_section = None  # Переменная для хранения текущего раздела данных
            for line in f:
                line = line.strip()
                if line == "Customers:":
                    current_section = "Customers"  # Установка текущего раздела данных
                elif line == "Loyalty Points:":
                    current_section = "Loyalty Points"  # Установка текущего раздела данных
                elif line == "Discount Info:":
                    current_section = "Discount Info"  # Установка текущего раздела данных
                else:
                    if current_section == "Customers":
                        # Разбивка строки на номер телефона, имя и фамилию посетителя
                        phone_number, first_name, last_name = line.split(",")
                        visitor = Visitor(phone_number, first_name, last_name)  # Создание объекта Visitor
                        self.customers.append(visitor)  # Добавление посетителя в список
                    elif current_section == "Loyalty Points":
                        phone_number, points = line.split(",")
                        self.loyalty_points[phone_number] = int(points)  # Добавление баллов лояльности в словарь
                    elif current_section == "Discount Info":
                        phone_number, discount_info = line.split(",", 1)
                        self.discount_info[phone_number] = discount_info  # Добавление информации о скидке в словарь
    

class VisitorMenu:
    def __init__(self, visitor_database):
        self.visitor_database = visitor_database

    def open_menu(self):

    # Меню управления информацией о клиенте
    
        options = {
            "1": self.add_visitor,
            "2": self.remove_visitor,
            "3": self.add_loyalty_points,
            "4": self.use_loyalty_points,
            "5": self.view_loyalty_points,
            "6": self.add_discount,
            "7": self.remove_discount,
            "8": self.print_visitor_list,
            "9": lambda: None
        }
        while True:
            print("______ Меню управления информацией о клиенте ______")
            print("Опции:\n"
                  "  1 - Добавить пользователя\n"
                  "  2 - Удалить пользователя\n"
                  "  3 - Добавить баллы лояльности\n"
                  "  4 - Использовать баллы лояльности\n"
                  "  5 - Посмотреть баллы лояльности\n"
                  "  6 - Добавить скидку\n"
                  "  7 - Удалить скидку\n"
                  "  8 - Вывести список пользователей\n"
                  "  9 - Выйти из меню")

            command = input("Введите номер опции: ")

            if command in options:
                options[command]()
                if command == "9":
                    return
            else:
                print("Неверная команда. Пожалуйста, выберите опцию от 1 до 9.")

    def add_visitor(self):
        phone_number = input("Введите номер телефона клиента: ")
        first_name = input("Введите имя клиента: ")
        last_name = input("Введите фамилию клиента: ")
        self.visitor_database.add_visitor(phone_number, first_name, last_name)
        print("Клиент успешно добавлен.")

    def remove_visitor(self):
        phone_number = input("Введите номер телефона клиента, которого необходимо удалить: ")
        self.visitor_database.remove_visitor(phone_number)
        print("Клиент успешно удален.")

    def add_loyalty_points(self):
        phone_number = input("Введите номер телефона клиента: ")
        points = int(input("Введите количество баллов лояльности для добавления: "))
        self.visitor_database.increase_loyalty_points(phone_number, points)
        print("Баллы лояльности успешно добавлены.")

    def use_loyalty_points(self):
        phone_number = input("Введите номер телефона клиента: ")
        points = int(input("Введите количество баллов лояльности для использования: "))
        if self.visitor_database.use_loyalty_points(phone_number, points):
            print("Баллы лояльности успешно использованы.")
        else:
            print("У клиента недостаточно баллов лояльности.")

    def view_loyalty_points(self):
        phone_number = input("Введите номер телефона клиента: ")
        points = self.visitor_database.get_loyalty_points(phone_number)
        print(f"Количество баллов лояльности: {points}")

    def add_discount(self):
        phone_number = input("Введите номер телефона клиента: ")
        discount_info = input("Введите информацию о скидке: ")
        self.visitor_database.add_discount(phone_number, discount_info)
        print("Информация о скидке успешно добавлена.")

    def remove_discount(self):
        phone_number = input("Введите номер телефона клиента: ")
        if self.visitor_database.check_discount_validity(phone_number):
            self.visitor_database.discount_info.pop(phone_number)
            print("Информация о скидке успешно удалена.")
        else:
            print("У клиента нет информации о скидке.")

    def print_visitor_list(self):
        print("Список клиентов:")
        for visitor in self.visitor_database.customers:
            print(f"Номер телефона: {visitor.phone_number}, Имя: {visitor.first_name}, Фамилия: {visitor.last_name}")


# Пример использования
# database = VisitorDatabase("database.txt")
# menu = VisitorMenu(database)
# menu.open_menu()
