#1 Именованный аргумент добавить пробелы и точку
def make_sentence(words=["This", "is", "a", "sentence"]):
    return " ".join(words) + "."
print(make_sentence(["This", "is", "a", "sentence"]))
#2 Позиционный аргумент
def sum_of_squares(*args):
    return sum(x**2 for x in args)
print(sum_of_squares(6))
#3 2 Именованных аргументов
def greet(name, language = "en"):
    greeting ={
        "en": f"Hello, {name}!",
        "ru": f"Привет, {name}!",
        "fr": f"Bonjour, {name}!",
    }
    return greeting.get(language,f"Hello, {name}!")
print(greet(name="Ilya", language="ru"))
#4 print_info
def print_info(**kwargs):
    if not kwargs:
        print("No info given.")
    else:
        for key, value in kwargs.items():
            print(f"{key}: {value}")
print_info(name="Ilya",age=25 ,city="Minsk")
#5 print_table
def print_table(**kwargs):
    if not kwargs:
        print("No info given.")
    else:
        print(f"{'Key' :<5} | {'Value' :<5}")
        print("-" * 15)
        for key, value in kwargs.items():
            print(f"{key:<5} | {value:<5}")
print_table(name="Ilya",age=25 ,city="Minsk")
#6 calculate
from functools import reduce
def calculate(*args, operation="+"):
    if not args:
        return 0
    ops = {
        "+" : lambda a, b: a + b,
        "-" : lambda a, b: a - b,
        "*" : lambda a, b: a * b,
        "/" : lambda a, b: a / b,
    }
    func = ops.get(operation, ops ["+"] )
    return reduce (func, args)
print(calculate(3,3,3,operation = "*"))
#7 print_triangle
def print_triangle(height = 5):
    for i in range (1, height + 1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(f"{spaces}{stars}")
print_triangle(7)
#8 create_post
def create_post(title,content,author,category="general"):
    post = {
        "title": title,
        "content": content,
        "author": author,
        "category": category,
    }
    return post
print(create_post("Python","Упражнения","Igor","IT"))
#9 create_product
def create_product(name,price,category,rating=0):
    product = {
        "name": name,
        "category": category,
        "price": price,
        "rating": rating,
    }
    return product
print(create_product("Молоко","Молочная продукция","2,98", 5))
#10 create_student
def create_student(name,last_name,surname,group,**kwargs):
    student = {
        "name": name,
        "last_name": last_name,
        "surname": surname,
        "group": group,
    }
    student.update(kwargs)
    return student
print(create_student("Илья","Сосновский","Игоревич","558-Дтк",phone=8034034343))
