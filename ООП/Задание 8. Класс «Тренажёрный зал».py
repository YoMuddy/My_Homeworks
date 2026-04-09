class Gym:
    def __init__(self, name):
        self.name = name
        self.clients = []

    def add_client(self, name,age):
        """Добавляет нового клиента"""
        client = {"name": name, "age": age, "active": False}
        self.clients.append(client)
        print(f"Клиет {name} добавлен в базу данных '{self.name}'.")

    def remove_client(self, name):
        """Удаляем клиента по имени"""
        self.clients = [c for c in self.clients if c ["name"] != name]
        print(f"Клиент {name} удален.")

    def activate_membership(self,name):
        """Активируем абонемент"""
        for client in self.clients:
            if client["name"] == name:
                client["active"] = True
                print(f"Абонемент для {name} активирован")
                return
        print(f"Клиент {name} не найден")

    def deactivate_membership(self,name):
        """Деактивируем абонемент"""
        for client in self.clients:
            if client["name"] == name:
                client["active"] = False
                print(f"Абонемент для {name} деактивирован")
                return

    def get_active_members(self):
        """Возвращает только тех, у кого active == True."""
        return [c for c in self.clients if c["active"]]

    def find_youngest_client(self):
        """Самый молодой клиент"""
        if not self.clients: return None
        return min(self.clients, key=lambda c: c["age"])

    def find_oldest_client(self):
        """Самый старший клиент"""
        if not self.clients: return None
        return max(self.clients, key=lambda c: c["age"])

    def average_age(self):
        """Средний возраст всех клиентов."""
        if not self.clients: return 0
        total_age = sum(c["age"] for c in self.clients)
        return total_age / len(self.clients)

my_gym = Gym("Качалка у Пети")

my_gym.add_client("Валерия", 24)
my_gym.add_client("Геннадий",38)
my_gym.add_client("Николай", 19)

my_gym.activate_membership("Валерия")

print(f"Средний возраст: {my_gym.average_age():.1f}")

youngest = my_gym.find_youngest_client()
oldest = my_gym.find_oldest_client()

print(f"Самый молодой клиент: {youngest ['name']} {youngest ['age']} лет")
print(f"Самый старший клиент: {oldest ['name']} {oldest ['age']}")

active = my_gym.get_active_members()

print(f"Активных клиентов: {len(active)}")
