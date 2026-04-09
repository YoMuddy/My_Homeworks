class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []
        self.status = "новый"

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item["price"] * item["quantity"]
        return total

    def add_item(self, name, price, quantity):
        new_item = {"name": name, "price": price, "quantity": quantity}
        self.items.append(new_item)

    def remove_item(self, name):
        self.items = [item for item in self.items if not item["name"] == name]

    def change_status(self, status):
        self.status = status

    def __str__(self):
        return f"Заказ №{self.order_id} ({self.status}). Итого: {self.calculate_total():.2f} руб."


class OrderSystem:
    def __init__(self):
        self.orders = []

    def create_order(self, order_id):
        new_order = Order(order_id)
        self.orders.append(new_order)
        return new_order

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def get_total_revenue(self):
        revenue = 0
        for order in self.orders:
            if order.status == "завершён":
                revenue += order.calculate_total()
        return revenue

    def list_orders(self):
        if not self.orders:
            print("Заказов пока нет.")
        else:
            for order in self.orders:
                print(order)


system = OrderSystem()


my_order = system.create_order(101)
my_order.add_item("Пицца", 550.0, 2)
my_order.add_item("Сок", 120.555, 1)

my_order.remove_item("Сок")

my_order.change_status("завершён")

system.list_orders()
print(f"Общая выручка системы: {system.get_total_revenue():.2f}")
