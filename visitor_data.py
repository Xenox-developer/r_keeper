from dataclasses import dataclass


@dataclass
class Visitor:
    id: int  # Идентификатор посетителя
    first_name: str  # Имя посетителя
    last_name: str  # Фамилия посетителя
    contact_info: str  # Контактная информация посетителя


class VisitorDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file # Путь к файлу базы данных
        self.visitors = []  # Список объектов Visitor для хранения информации о посетителях
        self.loyalty_points = {}  # Словарь для хранения баллов лояльности посетителей
        self.registration_info = {}  # Словарь для хранения информации о регистрации посетителей
        self.discount_info = {}  # Словарь для хранения информации о предоставленных скидках
        self.load_data()  # Загрузка данных из файла при инициализации объекта класса
    
    def add_visitor(self, visitor: Visitor):
        self.visitors.append(visitor)  # Добавление нового посетителя в список

    def remove_visitor(self, visitor_id: int):
        for visitor in self.visitors:
            if visitor.id == visitor_id:
                self.visitors.remove(visitor)  # Удаление посетителя из списка
                break
        if visitor_id in self.loyalty_points:
            del self.loyalty_points[visitor_id]  # Удаление баллов лояльности посетителя, если они есть
        if visitor_id in self.registration_info:
            del self.registration_info[visitor_id]  # Удаление информации о регистрации посетителя, если она есть
        if visitor_id in self.discount_info:
            del self.discount_info[visitor_id]  # Удаление информации о предоставленных скидках посетителя, если она есть

    def get_visitor_info(self, visitor_id: int):
        for visitor in self.visitors:
            if visitor.id == visitor_id:
                return visitor  # Возвращает информацию о посетителе по его идентификатору
        return None

    def add_loyalty_points(self, visitor_id: int, points: int):
        if visitor_id in self.loyalty_points:
            self.loyalty_points[visitor_id] += points  # Увеличение количества баллов лояльности у посетителя, если он уже существует
        else:
            self.loyalty_points[visitor_id] = points  # Начисление баллов лояльности посетителю, если он новый

    def use_loyalty_points(self, visitor_id: int, points: int):
        if visitor_id in self.loyalty_points:
            if self.loyalty_points[visitor_id] >= points:
                self.loyalty_points[visitor_id] -= points  # Списание определенного количества баллов лояльности у посетителя для предоставления скидки
                return True
        return False

    def add_discount_info(self, visitor_id: int, discount_info: dict):
        self.discount_info[visitor_id] = discount_info  # Добавление информации о предоставленной скидке для конкретного посетителя

    def check_discount_validity(self, visitor_id: int):
        if visitor_id in self.discount_info:
            # Здесь можно добавить логику для проверки действительности скидки
            return True  # Проверка, действительна ли скидка для данного посетителя
        return False

    def save_data(self):
        # Сохранение данных в файл
        with open(self.db_file, 'w') as f:
            for visitor in self.visitors:
                visitor_data = f"{visitor.id}\t{visitor.first_name}\t{visitor.last_name}\t{visitor.contact_info}\n"
                f.write(visitor_data)  # Запись информации о посетителях в файл, разделяя атрибуты символом табуляции

    def load_data(self):
        # Загрузка данных из файла
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    data = line.strip().split('\t')
                    visitor = Visitor(int(data[0]), data[1], data[2], data[3])
                    self.visitors.append(visitor)  # Чтение данных из файла и создание объектов Visitor для каждого посетителя
        except FileNotFoundError:
            pass  # Если файл не найден, пропускаем загрузку данных
