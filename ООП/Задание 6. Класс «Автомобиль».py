from datetime import datetime

class Car:
    def __init__(self, brand, model, year, fuel=0, mileage=0):
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel = fuel
        self.mileage = mileage

    def __check_fuel(self, distance):
        """Приватный метод: проверяет, хватит ли топлива"""
        required_fuel = distance * 0.1
        return self.fuel >= required_fuel

    def drive(self, distance):
        """Увеличивает пробег и тратит топливо (0.1 л на 1 км)."""
        if self.__check_fuel(distance):
            self.mileage += distance
            self.fuel -= distance * 0.1
            print(f"Проехали {distance} км.")
        else:
            print("Недостаточно топлива для поездки!")

    def refuel(self, liters):
        """Заправка автомобиля."""
        self.fuel += liters
        print(f"Заправлено {liters} л. Текущий уровень: {self.fuel} л.")

    def info(self):
        """Выводит состояние автомобиля."""
        print(f"--- {self.brand} {self.model} ---")
        print(f"Год: {self.year}, Пробег: {self.mileage} км, Топливо: {self.fuel} л.")

    def age(self):
        """Возвращает возраст автомобиля."""
        current_year = datetime.now().year
        return current_year - self.year

    @classmethod
    def from_string(cls, data):
        """Создает объект из строки 'Марка, Модель, Год'."""
        brand, model, year = data.split(", ")
        return cls(brand, model, int(year))

my_car = Car.from_string("Volkswagen, Passat, 2004")

my_car.refuel(50)
my_car.drive(100)
my_car.info()
print(f"Возраст авто: {my_car.age()} лет")

