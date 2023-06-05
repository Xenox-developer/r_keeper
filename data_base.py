import pickle
from dataclasses import dataclass
from typing import Dict


@dataclass
class Bill:
    Id: int
    date: str
    dishes_list: Dict[str, list[int, int]]
    total_summ: int


class SalesDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.sales_data = []
        self.load_data()

    def add_bill(self, bill: Bill):
        self.sales_data.append(bill)
        self.save_data()

    def get_sale_by_index(self, index: int):
        # Получение информации о чеке по его индексу в списке
        if not isinstance(index, int):
            raise TypeError('Index must be an integer')
        if 0 <= index < len(self.sales_data):
            return self.sales_data[index]
        else:
            return None

    def get_all_sales(self):
        # Получение информации о всех чеках
        return self.sales_data

    def print_sale(self, bill: Bill):
        # Вывод информации о конкретном чеке
        if not isinstance(bill, Bill):
            raise TypeError('Bill must be an instance of the Bill class')
        print(f"Date: {bill.date}nDishes: {bill.dishes_list}nTotal Sum: {bill.total_summ}")

    def print_all_sales(self):
        # Вывод информации о всех чеках
        for i, bill in enumerate(self.sales_data):
            print(f"Sale {i + 1}:")
            self.print_sale(bill)
            print()

    def save_data(self):
        # Сохранение данных в файл
        with open(self.db_file, 'w') as f:
            for bill in self.sales_data:
                f.write(f"{bill.Id}t{bill.date}t{bill.dishes_list}t{bill.total_summ}n")

    def load_data(self):
        # Загрузка данных из файла
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    data = line.strip().split('t')
                    bill = Bill(int(data[0]), data[1], eval(data[2]), int(data[3]))
                    self.sales_data.append(bill)
        except FileNotFoundError:
            pass
