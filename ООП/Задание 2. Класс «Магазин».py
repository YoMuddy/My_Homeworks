class Store:
    def __init__(self,store_name):
        self.store_name = store_name
        self.products = []

    def add_product(self, name, price, quantity):
        """Добавляет товар в магазин. Если товар с таким именем уже есть, увеличивает его количество."""
        for product in self.products:
            if product["name"] == name:
                product["quantity"] += quantity
                return
        self.products.append({"name": name, "price": price, "quantity": quantity})

    def remove_product(self, name):
        """Удаляет товар по имени"""
        self.products = [p for p in self.products if p ["name"] != name]

    def update_price(self, name, new_price):
        """Изменяет цену товара"""
        for product in self.products:
            if product["name"] == name:
                product["price"] = new_price
                break

    def sell_product(self, name, quantity):
        """Продает указанное колл-во товара"""
        for product in self.products:
            if product["name"] == name:
                if product["quantity"] >= quantity:
                    product["quantity"] -= quantity
                    print(f"Продано: {quantity} шт.товара {name}")
                else:
                    print("Недостаточно товара {name} на складе")
                return
        print(f"Товар {name} не найден")

    def get_inventory(self):
        """Возращает список всех товаров и их колл-во"""
        return [(p["name"],p["quantity"]) for p in self.products]

    def find_most_expensive(self):
        """Возращает самый дорогой товар"""
        if not self.products:
            return None
        return max(self.products, key=lambda x: x["price"])
    
    def find_cheapest(self):
        """Возращает самый дешевый товар"""
        if not self.products:
            return None
        return min(self.products, key=lambda x: x["price"])

my_store = Store("Копеечка")
my_store.add_product("Бананы",50,100)
my_store.add_product("Яблоки", 30,50)
my_store.update_price("Яблоки",40)
my_store.sell_product("Бананы",6)

print(f"Инвентарь:", my_store.get_inventory())
print(f"Самый дорогой товар:", my_store.find_most_expensive())
print(f"Самый дешевый товар:", my_store.find_cheapest())
