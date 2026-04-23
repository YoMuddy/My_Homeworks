import uuid
from datetime import datetime
from peewee import *

# Создаем файл базы данных
db = SqliteDatabase('not_a_shop.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    points = IntegerField(default=0)

    # Статичный метод проверки пользователя (стр. 3 PDF)
    @staticmethod
    def is_exists(username):
        try:
            Users.get(Users.username == username)
            return True
        except DoesNotExist:
            return False

class Products(BaseModel):
    name = CharField()
    cost = IntegerField()
    count = IntegerField()

class Tickets(BaseModel):
    uuid = CharField(unique=True)
    available = BooleanField(default=True)
    user = ForeignKeyField(Users, backref='tickets', null=True)

    @staticmethod
    def valid_ticket(ticket_uuid):
        try:
            ticket = Tickets.get(Tickets.uuid == ticket_uuid, Tickets.available == True)
            return ticket
        except DoesNotExist:
            return None

class Orders(BaseModel):
    user = ForeignKeyField(Users, backref='orders')
    product = ForeignKeyField(Products, backref='orders')
    count = IntegerField()
    order_datetime = DateTimeField(default=datetime.now)

# Создаем таблицы в файле
db.connect()
db.create_tables([Users, Products, Tickets, Orders])

current_user = None  # Глобальная переменная для авторизации

def show_products():
    print(f"\n{'ID':<5} {'Стоимость':<12} {'Кол-во':<10} {'Название'}")
    print("="*50)
    for p in Products.select().where(Products.count > 0):
        print(f"{p.id:<5} {p.cost:<12} {p.count:<10} {p.name}")

def register():
    login = input("Введите логин > ")
    if Users.is_exists(login):
        print("Такой пользователь уже есть!")
    else:
        password = input("Введите пароль > ")
        user = Users.create(username=login, password=password)
        print("Регистрация успешна!")
        return user

def login_user():
    login = input("Введите логин > ")
    password = input("Введите пароль > ")
    try:
        user = Users.get(Users.username == login, Users.password == password)
        print(f"Привет, {user.username}!")
        return user
    except DoesNotExist:
        print("Неверный логин или пароль!")
        return None


def seed_data():
    # Добавляем товары, если их нет
    if Products.select().count() == 0:
        Products.create(name="Картинка с котиком", cost=20, count=50)
        Products.create(name="Наклейка синего цвета", cost=15, count=45)
        Products.create(name="Игральные кости (белые)", cost=25, count=40)

    # Добавляем один тестовый тикет для проверки (стр. 5 PDF)
    if Tickets.select().count() == 0:
        Tickets.create(uuid="ebb94499-05c9-494f-9f4a-402c6543f244", available=True)


seed_data()


def buy_product(user):
    # Запрашиваем ввод в формате "ID количество" (стр. 7 PDF)
    raw_input = input("Введите [ID товара] [Количество] через пробел: ").split()

    if len(raw_input) < 2:
        print("Ошибка! Нужно ввести два числа через пробел.")
        return

    try:
        p_id = int(raw_input[0])
        qnt = int(raw_input[1])

        # Ищем товар
        product = Products.get_by_id(p_id)
        total_cost = product.cost * qnt

        if product.count < qnt:
            print(f"На складе нет столько товара! Доступно: {product.count}")
        elif user.points < total_cost:
            print(f"Недостаточно поинтов! Нужно: {total_cost}, у вас: {user.points}")
        else:
            # Совершаем сделку
            product.count -= qnt
            product.save()

            user.points -= total_cost
            user.save()

            # Записываем в историю (стр. 8 PDF)
            Orders.create(user=user, product=product, count=qnt)
            print(f"Успешно куплено: {product.name} ({qnt} шт.)")

    except DoesNotExist:
        print("Товар с таким ID не найден.")
    except ValueError:
        print("Введите корректные числа.")


def show_profile(user):
    print(f"\n--- ПРОФИЛЬ: {user.username} ---")
    print(f"Баланс: {user.points} поинтов")
    print("\nИстория заказов:")
    print(f"{'Дата':<18} {'Товар':<20} {'Кол-во':<7} {'Сумма'}")
    print("-" * 55)

    # Получаем все заказы пользователя (связь backref='orders' из Шага 1)
    orders = user.orders
    for o in orders:
        date = o.order_datetime.strftime("%d.%m %H:%M")
        total = o.count * o.product.cost
        print(f"{date:<18} {o.product.name:<20} {o.count:<7} {total}")


while True:
    if not current_user:
        print("\n=== Добро пожаловать в 'Не магазин' ===")
        print("> Товары\n> Зарегистрироваться\n> Войти")
        cmd = input("\nВведите команду: ").lower()

        if cmd == "товары":
            show_products()
        elif cmd == "зарегистрироваться":
            current_user = register()
        elif cmd == "войти":
            current_user = login_user()
    else:
        print(f"\n=== Вы вошли как {current_user.username} (Поинты: {current_user.points}) ===")
        print("> Товары\n> Купить\n> Профиль\n> Тикет\n> Выход")
        cmd = input("\nВведите команду: ").lower()

        if cmd == "товары":
            show_products()
        elif cmd == "купить":
            buy_product(current_user)  # Теперь это заработает
        elif cmd == "профиль":
            show_profile(current_user) # И это тоже
        elif cmd == "тикет":
            code = input("Введите UUID тикета: ")
            ticket = Tickets.valid_ticket(code)
            if ticket:
                ticket.available = False
                ticket.user = current_user
                ticket.save()
                current_user.points += 20
                current_user.save()
                print("Вы успешно обменяли тикет на 20 поинтов!")
            else:
                print("Тикет недействителен или уже использован.")
        elif cmd == "выход":
            current_user = None
