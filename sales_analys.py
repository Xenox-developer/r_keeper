# класс SalesAnalysis, который будет содержать методы для анализа продаж.

class SalesAnalysis:
    def __init__(self, sales_data):
        self.sales_data = sales_data

    def total_revenue(self):
        # Расчет общей выручки на основе данных о продажах
        revenue = sum([sale['price'] for sale in self.sales_data])
        return revenue

    def popular_dishes(self, num_dishes):
        # Расчет наиболее популярных блюд на основе данных о продажах
        dishes = {}
        for sale in self.sales_data:
            dish = sale['dish']
            if dish in dishes:
                dishes[dish] += 1
            else:
                dishes[dish] = 1
        sorted_dishes = sorted(dishes.items(), key=lambda x: x[1], reverse=True)
        return sorted_dishes[:num_dishes]

    def sales_statistics(self):
        # Расчет статистики продаж на основе данных о продажах
        num_sales = len(self.sales_data)
        avg_sale = sum([sale['price'] for sale in self.sales_data]) / num_sales
        min_sale = min([sale['price'] for sale in self.sales_data])
        max_sale = max([sale['price'] for sale in self.sales_data])
        return {'num_sales': num_sales, 'avg_sale': avg_sale, 'min_sale': min_sale, 'max_sale': max_sale}

# Для интеграции с внешними системами поставок
# есть сторонняя система, которая содержит данные о поставках,
# класс ShippingAdapter, который будет адаптировать данные
# о поставках для использования в классе SalesAnalysis.


class ShippingAdapter:
    def __init__(self, shipping_data):
        self.shipping_data = shipping_data

    def get_shipments(self, start_date, end_date):
        # Получение данных о поставках за заданный период времени
        shipments = []
        for shipment in self.shipping_data:
            if start_date <= shipment['date'] <= end_date:
                shipments.append(shipment)
        return shipments


# класс SalesFacade, который будет предоставлять методы для выполнения
# всех анализов продаж, используя классы SalesAnalysis и ShippingAdapter.

class SalesFacade:
    def __init__(self, sales_data, shipping_data):
        self.sales_analysis = SalesAnalysis(sales_data)
        self.shipping_adapter = ShippingAdapter(shipping_data)

    def total_revenue(self):
        # Расчет общей выручки на основе данных о продажах
        return self.sales_analysis.total_revenue()

    def popular_dishes(self, num_dishes):
        # Расчет наиболее популярных блюд на основе данных о продажах
        return self.sales_analysis.popular_dishes(num_dishes)

    def sales_statistics(self):
        # Расчет статистики продаж на основе данных о продажах
        return self.sales_analysis.sales_statistics()

    def shipping_statistics(self, start_date, end_date):
        # Расчет статистики поставок на основе данных о поставках
        shipments = self.shipping_adapter.get_shipments(start_date, end_date)
        num_shipments = len(shipments)
        avg_shipment = sum([shipment['price'] for shipment in shipments]) / num_shipments
        min_shipment = min([shipment['price'] for shipment in shipments])
        max_shipment = max([shipment['price'] for shipment in shipments])
        return {'num_shipments': num_shipments, 'avg_shipment': avg_shipment,
                'min_shipment': min_shipment, 'max_shipment': max_shipment}
