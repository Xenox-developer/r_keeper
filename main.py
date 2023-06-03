import Kitchen_class
import Orders
import Menu_class


def tick(kitchen: Kitchen_class.CookingTerminal):
    end = ''
    while end != 'end':
        kitchen.tick()
        kitchen.get_info()
        end = input()


menu = Menu_class.Menu('menu_file.txt')
tem = Kitchen_class.CookingTerminal()
tem.add_performer(['Супы', 'Салаты', 'Закуски'])
orders = Orders.OrderTerminal()
tem.set_menu(menu)
orders.set_menu(menu)
orders.open_menu()
tick(tem)
orders.open_menu()