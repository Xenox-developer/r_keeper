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
