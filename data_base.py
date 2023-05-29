import pickle

class SalesDatabase:
    def __init__(self, db_file: str = 'sales_db.pkl'):
        self.db_file = db_file
        self.sales_data = []

    def add_sale(self, date: str, dish: str, price: float):
        # Добавление информации о чеке в базу данных
        sale = {'date': date, 'dish': dish, 'price': price}
        self.sales_data.append(sale)
        self.save_data()

    def get_sale_by_index(self, index: int):
        # Получение информации о чеке по его индексу в списке
        if 0 <= index < len(self.sales_data):
            return self.sales_data[index]
        else:
            return None

    def get_all_sales(self):
        # Получение информации о всех чеках
        return self.sales_data

    def print_sale(self, sale: dict):
        # Вывод информации о конкретном чеке
        print(f"Date: {sale['date']}nDish: {sale['dish']}nPrice: {sale['price']}")

    def print_all_sales(self):
        # Вывод информации о всех чеках
        for i, sale in enumerate(self.sales_data):
            print(f"Sale {i + 1}:")
            self.print_sale(sale)
            print()

    def save_data(self):
        # Сохранение данных в файл
        with open(self.db_file, 'wb') as f:
            pickle.dump(self.sales_data, f)

    def load_data(self):
        # Загрузка данных из файла
        try:
            with open(self.db_file, 'rb') as f:
                self.sales_data = pickle.load(f)
        except FileNotFoundError:
            pass
