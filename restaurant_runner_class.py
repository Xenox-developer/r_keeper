
class RestaurantRunner:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(RestaurantRunner, cls).__new__(cls)
        return cls._instance

    def connect_orders_terminal(self, item: 'OrderTerminal'):
        self.order_terminal = item

    def connect_cooking_terminal(self, item: 'CookingTerminal'):
        self.cooking_terminal = item

    def send_ready_dishes(self, ready_dishes: list[str, list[int]]):
        if not hasattr(self, 'order_terminal'):
            print('К посланцу не подключён терминал заказов')
            return
        self.order_terminal.get_ready_dishes(ready_dishes)

    def send_order_tasks(self, order):
        if not hasattr(self, 'cooking_terminal'):
            print('К посланцу не подключён терминал готовки')
            return

        self.cooking_terminal.add_tasks(order)
