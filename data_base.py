import sqlite3

class SalesDatabase:
    def __init__(self, db_name='sales.db'):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        # Подключение к базе данных
        self.connection = sqlite3.connect(self.db_name)

    def create_table(self):
        # Создание таблицы для хранения информации о чеках
        query = '''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            dish TEXT,
            price REAL
        );
        '''
        self.connection.execute(query)

    def add_sale(self, date, dish, price):
        # Добавление информации о чеке в таблицу
        query = '''
        INSERT INTO sales (date, dish, price)
        VALUES (?, ?, ?);
        '''
        self.connection.execute(query, (date, dish, price))
        self.connection.commit()

    def get_sale_by_id(self, sale_id):
        # Получение информации о чеке по его идентификатору
        query = '''
        SELECT * FROM sales WHERE id = ?;
        '''
        cursor = self.connection.execute(query, (sale_id,))
        return cursor.fetchone()

    def get_all_sales(self):
        # Получение информации о всех чеках
        query = '''
        SELECT * FROM sales;
        '''
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def print_sale(self, sale):
        # Вывод информации о конкретном чеке
        print(f"ID: {sale[0]}nDate: {sale[1]}nDish: {sale[2]}nPrice: {sale[3]}")

    def print_all_sales(self):
        # Вывод информации о всех чеках
        sales = self.get_all_sales()
        for sale in sales:
            self.print_sale(sale)

    def close(self):
        # Закрытие соединения с базой данных
        self.connection.close()
