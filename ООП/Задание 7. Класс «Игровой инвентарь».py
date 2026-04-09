class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, name, weight, value):
        """Создает словарь предмета и добавляет его в список."""
        item = {
            "name": name,
            "weight": weight,
            "value": value
        }
        self.items.append(item)
        print(f"✅ Предмет '{name}' добавлен в инвентарь.")

    def remove_item(self, name):
        """Удаляет все предметы с указанным именем через фильтрацию списка."""
        self.items = [item for item in self.items if item["name"] != name]
        print(f"❌ Предмет '{name}' удален.")

    def get_total_weight(self):
        """Считает сумму всех значений по ключу 'weight'."""
        return sum(item["weight"] for item in self.items)

    def get_total_value(self):
        """Считает сумму всех значений по ключу 'value'."""
        return sum(item["value"] for item in self.items)

    def find_heaviest(self):
        """Ищет словарь с максимальным весом. Если пусто — вернет None."""
        if not self.items:
            return None
        return max(self.items, key=lambda x: x["weight"])

    def find_most_valuable(self):
        """Ищет словарь с максимальной стоимостью."""
        if not self.items:
            return None
        return max(self.items, key=lambda x: x["value"])

    def sort_by_value(self, reverse=True):
        """Возвращает НОВЫЙ отсортированный список по цене."""
        return sorted(self.items, key=lambda x: x["value"], reverse=reverse)

    def sort_by_weight(self, reverse=True):
        """Возвращает НОВЫЙ отсортированный список по весу."""
        return sorted(self.items, key=lambda x: x["weight"], reverse=reverse)


player_inv = Inventory()

player_inv.add_item("Меч", 5, 100)
player_inv.add_item("Щит", 8, 150)
player_inv.add_item("Зелье", 1, 50)

print(f"\nОбщий вес: {player_inv.get_total_weight()} кг")
print(f"Общая ценность: {player_inv.get_total_value()} золота")

top_item = player_inv.find_most_valuable()
if top_item:
    print(f"Самый дорогой предмет: {top_item['name']} ({top_item['value']} золота)")

print("\n📦 Инвентарь (от тяжелых к легким):")
for item in player_inv.sort_by_weight():
    print(f" - {item['name']}: {item['weight']} кг")
player_inv.remove_item("Зелье")

for item in player_inv.items:
    print(item["name"])
