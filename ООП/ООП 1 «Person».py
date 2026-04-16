class Person:
    def __init__(self,name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender
    def __str__(self):
        return f"Имя: {self.name}, Возраст: {self.age}, Пол: {self.gender} "
    def get_name(self):
        return self.name
    @property
    def set_name(self):
        return self.name
    @set_name.setter
    def set_name(self,new_name):
        self.name = new_name
    @staticmethod
    def is_adult(age):
        return age >= 18
    @classmethod
    def create_from_string(cls, s):
        name, age, gender = s.split("-")
        return cls(name,int(age),gender)

p = Person.create_from_string("Илья-25-мужской")
print(p)
p.set_name = "Игорь"
print(p.set_name)
print(Person.is_adult(p.age))
