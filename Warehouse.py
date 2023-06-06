from dataclasses import dataclass, field
from datetime import date
from typing import List

@dataclass
class Product:
    name: str
    category: str
    quantity: int
    price: float
    arrival_date: date
    expiration_date: date

@dataclass
class Order_product:
    id: int
    date: date
    product_list: List[Product] = field(default_factory=list)
    status: str = "В обработке"

class WarehouseManager:
    def __init__(self):
        self.products = []
        self.orders = []
        self.db_file = "data.txt"  # Имя файла для сохранения данных
    
    def add_product(self, product: Product):
        self.products.append(product)
        self.save_data()
    
    def remove_product(self, product: Product):
        self.products.remove(product)
        self.save_data()
    
    def get_all_products(self):
        return self.products
        
    
    def create_order(self, order: Order_product):
        self.orders.append(order)
    
    def change_order_status(self, order_id: int, new_status: str):
        for order in self.orders:
            if order.id == order_id:
                order.status = new_status
                break
    
    def get_all_orders(self):
        return self.orders
    
    def save_data(self):
        with open(self.db_file, 'w') as f:
            f.write("Products:\n")
            for product in self.products:
                f.write(f"{product.name},{product.category},{product.quantity},{product.price},{product.arrival_date},{product.expiration_date}\n")
            f.write("Orders:\n")
            for order in self.orders:
                products_str = ";".join([f"{p.name},{p.category},{p.quantity},{p.price},{p.arrival_date},{p.expiration_date}" for p in order.product_list])
                f.write(f"{order.id},{order.date},{products_str},{order.status}\n")

    def load_data(self):
        self.products = []
        self.orders = []
        with open(self.db_file, 'r') as f:
            current_section = None
            for line in f:
                line = line.strip()
                if line == "Products:":
                    current_section = "Products"
                elif line == "Orders:":
                    current_section = "Orders"
                else:
                    if current_section == "Products":
                        name, category, quantity, price, arrival_date, expiration_date = line.split(",")
                        product = Product(name, category, int(quantity), float(price), date.fromisoformat(arrival_date), date.fromisoformat(expiration_date))
                        self.products.append(product)
                    elif current_section == "Orders":
                        order_data = line.split(",")
                        order_id = int(order_data[0])
                        order_date = date.fromisoformat(order_data[1])
                        product_list = []
                        products_str = order_data[2].split(";")
                        for product_str in products_str:
                            product_info = product_str.split(",")
                            name, category, quantity, price, arrival_date, expiration_date = product_info
                            product = Product(name, category, int(quantity), float(price), date.fromisoformat(arrival_date), date.fromisoformat(expiration_date))
                            product_list.append(product)
                        order_status = order_data[3]
                        order = Order_product(order_id, order_date, product_list, order_status)
                        self.orders.append(order)


class WarehouseMenu:
    def __init__(self, warehouse_manager):
        self.warehouse_manager = warehouse_manager

    def open_menu(self):
        options = {
            "1": self.add_product,
            "2": self.remove_product,
            "3": self.get_all_products,
            "4": self.search_product,
            "5": self.create_order,
            "6": self.change_order_status,
            "7": self.get_all_orders,
            "8": self.search_order,
            "9": lambda: None
        }

        while True:
            print("______ Меню управления информацией о складе ______")
            print("Опции:\n"
                  "  1 - Добавить товар\n"
                  "  2 - Удалить товар\n"
                  "  3 - Получить список всех товаров\n"
                  "  4 - Поиск товара\n"
                  "  5 - Создание нового заказа\n"
                  "  6 - Изменение статуса заказа\n"
                  "  7 - Получить список всех заказов\n"
                  "  8 - Поиск заказа\n"
                  "  9 - Выйти из меню")

            command = input("Введите номер опции: ")

            if command in options:
                options[command]()
                if command == "9":
                    return
            else:
                print("Неверная команда. Пожалуйста, выберите опцию от 1 до 9.")

    def add_product(self):
        name = input("Введите название товара: ")
        category = input("Введите категорию товара: ")
        quantity = int(input("Введите количество товара: "))
        price = float(input("Введите цену товара: "))
        arrival_date = input("Введите дату поступления товара в формате ГГГГ-ММ-ДД: ")
        expiration_date = input("Введите дату истечения срока годности товара в формате ГГГГ-ММ-ДД: ")

        product = Product(name, category, quantity, price, date.fromisoformat(arrival_date), date.fromisoformat(expiration_date))
        self.warehouse_manager.add_product(product)
        print("Товар успешно добавлен.")

    def remove_product(self):
        products = self.warehouse_manager.get_all_products()
        if not products:
            print("На складе нет товаров.")
            return

        print("Список товаров:")
        for index, product in enumerate(products):
            print(f"{index+1}. {product.name} (Категория: {product.category}, Количество: {product.quantity}, Цена: {product.price})")

        selection = input("Введите номер товара для удаления: ")
        if not selection.isdigit() or int(selection) < 1 or int(selection) > len(products):
            print("Неверный номер товара.")
            return

        product = products[int(selection) - 1]
        self.warehouse_manager.remove_product(product)
        print("Товар успешно удален.")

    def get_all_products(self):
        products = self.warehouse_manager.get_all_products()
        if not products:
            print("На складе нет товаров.")
            return

        print("Список товаров:")
        for index, product in enumerate(products):
            print(f"{index+1}. {product.name} (Категория: {product.category}, Количество: {product.quantity}, Цена: {product.price})")

    def search_product(self):
        keyword = input("Введите ключевое слово для поиска товара: ")
        products = self.warehouse_manager.get_all_products()
        found_products = []

        for product in products:
            if keyword.lower() in product.name.lower() or keyword.lower() in product.category.lower():
                found_products.append(product)

        if not found_products:
            print("По вашему запросу ничего не найдено.")
            return

        print("Результаты поиска:")
        for index, product in enumerate(found_products):
            print(f"{index+1}. {product.name} (Категория: {product.category}, Количество: {product.quantity}, Цена: {product.price})")

    def create_order(self):
        order_id = int(input("Введите ID заказа: "))
        order_date = input("Введите дату заказа в формате ГГГГ-ММ-ДД: ")

        product_list = []
        while True:
            product_name = input("Введите название товара (или введите 'готово', чтобы завершить): ")
            if product_name.lower() == "готово":
                break

            products = self.warehouse_manager.get_all_products()
            found_products = []
            for product in products:
                if product.name.lower() == product_name.lower():
                    found_products.append(product)

            if not found_products:
                print("Товар с таким названием не найден.")
                continue

            if len(found_products) == 1:
                product = found_products[0]
                quantity = int(input("Введите количество товара: "))
                if quantity > product.quantity:
                    print("Недостаточное количество товара на складе.")
                    continue

                product_list.append(Product(product.name, product.category, quantity, product.price, product.arrival_date, product.expiration_date))
                print("Товар успешно добавлен в заказ.")
            else:
                print("Найдено несколько товаров с таким названием:")
                for index, product in enumerate(found_products):
                    print(f"{index+1}. {product.name} (Категория: {product.category}, Количество: {product.quantity}, Цена: {product.price})")

                selection = input("Введите номер товара для добавления в заказ: ")
                if not selection.isdigit() or int(selection) < 1 or int(selection) > len(found_products):
                    print("Неверный номер товара.")
                    continue

                product = found_products[int(selection) - 1]
                quantity = int(input("Введите количество товара: "))
                if quantity > product.quantity:
                    print("Недостаточное количество товара на складе.")
                    continue

                product_list.append(Product(product.name, product.category, quantity, product.price, product.arrival_date, product.expiration_date))
                print("Товар успешно добавлен в заказ.")

        order = Order_product(order_id, date.fromisoformat(order_date), product_list)
        self.warehouse_manager.create_order(order)
        print("Заказ успешно создан.")

    def change_order_status(self):
        orders = self.warehouse_manager.get_all_orders()
        if not orders:
            print("На складе нет заказов.")
            return

        print("Список заказов:")
        for index, order in enumerate(orders):
            print(f"{index+1}. Заказ ID: {order.id}, Дата: {order.date}, Статус: {order.status}")

        selection = input("Введите номер заказа для изменения статуса: ")
        if not selection.isdigit() or int(selection) < 1 or int(selection) > len(orders):
            print("Неверный номер заказа.")
            return

        order_id = orders[int(selection) - 1].id
        new_status = input("Введите новый статус заказа: ")
        self.warehouse_manager.change_order_status(order_id, new_status)
        print("Статус заказа успешно изменен.")

    def get_all_orders(self):
        orders = self.warehouse_manager.get_all_orders()
        if not orders:
            print("На складе нет заказов.")
            return

        print("Список заказов:")
        for index, order in enumerate(orders):
            print(f"{index+1}. Заказ ID: {order.id}, Дата: {order.date}, Статус: {order.status}")

    def search_order(self):
        keyword = input("Введите ключевое слово для поиска заказа: ")
        orders = self.warehouse_manager.get_all_orders()
        found_orders = []

        for order in orders:
            for product in order.product_list:
                if keyword.lower() in product.name.lower() or keyword.lower() in product.category.lower():
                    found_orders.append(order)
                    break

        if not found_orders:
            print("По вашему запросу ничего не найдено.")
            return

        print("Результаты поиска:")
        for index, order in enumerate(found_orders):
            print(f"{index+1}. Заказ ID: {order.id}, Дата: {order.date}, Статус: {order.status}")

# Пример использования
warehouse_manager = WarehouseManager()
menu = WarehouseMenu(warehouse_manager)
menu.open_menu()
