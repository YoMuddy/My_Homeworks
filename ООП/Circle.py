class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Этот метод нужен, чтобы при print() мы видели текст, а не адрес в памяти
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __sub__(self, other):
        # Вычисляем новый радиус по модулю
        new_r = abs(self.r - other.r)

        # Если радиус обнулился — возвращаем Точку
        if new_r == 0:
            return Point(self.x, self.y)

        # Иначе возвращаем новую Окружность
        return Circle(self.x, self.y, new_r)

    def __repr__(self):
        return f"Circle(x={self.x}, y={self.y}, r={self.r})"


# --- ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ---

c1 = Circle(10, 10, 20)  # Радиус 20
c2 = Circle(10, 10, 15)  # Радиус 15
c3 = Circle(5, 5, 20)  # Радиус 20

# 1. Вычитаем разные радиусы: 20 - 15 = 5 (получим Circle)
result1 = c1 - c2
print(f"Результат 1: {result1}")

# 2. Вычитаем одинаковые радиусы: 20 - 20 = 0 (получим Point)
result2 = c1 - c3
print(f"Результат 2: {result2}")
