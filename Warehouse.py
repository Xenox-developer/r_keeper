from datetime import datetime
from typing import List

class WarehouseManager:
    def __init__(self):
        self.warehouse = Warehouse()  # Создание объекта склада при инициализации менеджера

    def create_order(self, products: List[Product]) -> Order:
        """
        Создает новый заказ на основе переданных товаров и обрабатывает его на складе.

        Args:
            products: Список товаров для заказа.

        Returns:
            Созданный заказ.
        """
        order = Order(products)  # Создание объекта заказа на основе переданных товаров
        self.warehouse.process_order(order)  # Обработка заказа складом
        return order

    def change_order_status(self, order_id: int, new_status: str) -> bool:
        """
        Изменяет статус заказа по его идентификатору.

        Args:
            order_id: Идентификатор заказа.
            new_status: Новый статус заказа.

        Returns:
            True, если статус заказа успешно изменен, False в противном случае.
        """
        order = self.warehouse.get_order(order_id)  # Получение объекта заказа по идентификатору
        if order:
            order.status = new_status  # Изменение статуса заказа
            return True
        return False

    def get_inventory_report(self) -> List[Product]:
        """
        Возвращает отчет о товарах на складе.

        Returns:
            Список товаров на складе.
        """
        return self.warehouse.get_products()


class Product:
    def __init__(self, name: str, category: str, quantity: int, price: float,
                 arrival_date: datetime, expiration_date: datetime):
        """
        Инициализация объекта товара.

        Args:
            name: Название товара.
            category: Категория товара.
            quantity: Количество товара на складе.
            price: Цена за единицу товара.
            arrival_date: Дата поставки товара на склад.
            expiration_date: Срок годности товара.
        """
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.arrival_date = arrival_date
        self.expiration_date = expiration_date


class Order:
    def __init__(self, product_list: List[Product]):
        """
        Инициализация объекта заказа.

        Args:
            product_list: Список товаров и их количество в заказе.
        """
        self.id = self.generate_order_id()  # Генерация идентификатора заказа
        self.date = datetime.now()  # Дата оформления заказа (текущая дата и время)
        self.product_list = product_list  # Список товаров и их количество в заказе
        self.status = "New"  # Статус заказа (изначально "Новый")

    def generate_order_id(self):
        """
        Генерирует уникальный идентификатор заказа.

        Returns:
            Идентификатор заказа.
        """
        pass


class Warehouse:
    def __init__(self):
        self.product_list = []  # Список всех товаров на складе
        self.orders = []  # Список всех заказов на складе

    def add_product(self, product: Product):
        """
        Добавляет товар на склад.

        Args:
            product: Добавляемый товар.
        """
        self.product_list.append(product)

    def remove_product(self, product: Product):
        """
        Удаляет товар со склада.

        Args:
            product: Удаляемый товар.
        """
        self.product_list.remove(product)

    def get_orders(self) -> List[Order]:
        """
        Возвращает список всех заказов на складе.

        Returns:
            Список заказов на складе.
        """
        return self.orders

    def get_order(self, order_id: int) -> Order:
        """
        Возвращает заказ по его идентификатору.

        Args:
            order_id: Идентификатор заказа.

        Returns:
            Заказ с указанным идентификатором или None, если заказ не найден.
        """
        for order in self.orders:
            if order.id == order_id:
                return order
        return None

    def process_order(self, order: Order):
        """
        Обрабатывает заказ и добавляет его в список заказов.

        Args:
            order: Обрабатываемый заказ.
        """
        self.orders.append(order)

    def get_products(self) -> List[Product]:
        """
        Возвращает список всех товаров на складе.

        Returns:
            Список товаров на складе.
        """
        return self.product_list
