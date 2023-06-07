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
        print('Чек ID:', bill.Id)
        print(f"Date: {bill.date}\nDishes: ")
        for name in bill.dishes_list.keys():
            print(f'  {name}:{bill.dishes_list[name][0]}*{bill.dishes_list[name][1]}')
        print(f'Total summ:{bill.total_summ}')

    def print_all_sales(self):
        # Вывод информации о всех чеках
        for i, bill in enumerate(self.sales_data):
            self.print_sale(bill)
            print()

    def save_data(self):
        # Сохранение данных в файл
        with open(self.db_file, 'w', encoding='utf-8') as f:
            for bill in self.sales_data:
                f.write(f"{bill.Id}\t{bill.date}\t")
                for name in bill.dishes_list.keys():
                    f.write(f'{name}:{bill.dishes_list[name][0]}*{bill.dishes_list[name][0]}\t')
                f.write(f'{bill.total_summ}\n')


    def load_data(self):
        # Загрузка данных из файла
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                for line in f:
                    data = line.strip().split('\t')
                    dish_dic_data = data[2:len(data) - 1]
                    dish_dic = {}
                    for i in dish_dic_data:
                        data1 = list(i.split(':'))
                        count, price = map(int, data1[1].split('*'))
                        dish_dic[data1[0]] = [count, price]
                    bill = Bill(int(data[0]), data[1], dish_dic, int(data[len(data) - 1]))
                    self.sales_data.append(bill)
        except FileNotFoundError:
            pass

    def open_menu(self):
        while True:
            print('______ Меню базы данных ______')
            print('Опции: \n'
                  'save - сохранить данные в файл\n'
                  'print - вывести имеющиеся данные в терминал\n'
                  'close - выйти из меню')

            command = input().rstrip()

            if command == 'save':
                self.save_data()
                print('Сохранение произведено')
            elif command == 'print':
                self.print_all_sales()
            elif command == 'close':
                return
            else:
                print('Неизвестная команда')
