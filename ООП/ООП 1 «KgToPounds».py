class KgToPounds:
    def __init__(self,kg):
        self.set_kg(kg)

    def to_pounds(self):
        return self.__kg * 2.205

    def set_kg(self,new_kg):
        if isinstance(new_kg, (int, float)):
            self.__kg = new_kg

        else:
            print("Ошибка введите число")
    def get_kg(self):
        return self.__kg

converter = KgToPounds(10)
print(f"Кг: {converter.get_kg()}, Фунты: {converter.to_pounds()}")
converter.set_kg(20)
print(f"Новое значение кг: {converter.get_kg()}")

class KgToPounds:
    def __init__(self, kg):
        self.kg = kg

    def to_pounds(self):
        return self.__kg * 2.205

    @property
    def kg(self):
        return self.__kg

    @kg.setter
    def kg(self, new_kg):
        if isinstance(new_kg, (int, float)):
            self.__kg = new_kg

        else:
            print("Килограммы должны быть числом!")

converter_prop = KgToPounds(5)
print(f"Текущий вес: {converter_prop.kg}")
converter_prop.kg = 15
print(f"В фунтах: {converter_prop.to_pounds()}")
