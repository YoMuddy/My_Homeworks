import time

class Auto:
    def __init__(self, brand, age, mark, color=None, weight=None):
        self.brand = brand
        self.age = age
        self.mark = mark
        self.color = color
        self.weight= weight

    def move(self):
        print("move")

    def stop(self):
        print("stop")

    def birthday(self):
        self.age += 1

#Грузовик=======================
class Truck(Auto):
    def __init__(self, brand, age, mark,max_load,color=None, weight=None):
        super().__init__(brand, age, mark, color, weight)
        self.max_load = max_load
    def move(self):
        print("attention")
        super().move()
    def load(self):
        time.sleep(1)
        print("load")
        time.sleep(1)
#Легковое Авто==========
class Car(Auto):
    def __init__(self, brand, age, mark, max_speed, color=None, weight=None):
        super().__init__(brand, age, mark, color, weight)
        self.max_speed = max_speed
    def move(self):
        print(f"max speed is  {self.max_speed}")
        super().move()
#Грузовики
truck1 = Truck("Volvo", 5, "FH16", 20000, "Blue", 8000)
truck2 = Truck("KAMAZ", 2, "5490", 15000)

# Легковые
car1 = Car("Tesla", 1, "Model S", 250, "Red")
car2 = Car("Lada", 10, "Vesta", 180, "Silver", 1200)

print("Тест Грузовика 1")
truck1.move()
truck1.load()
print(f"Грузоподьемность: {truck1.max_load}")

print("Тест Автомобиля 1")
car1.move()
car1.birthday()
print(f"Возраст автомобиля: {car1.age}")
