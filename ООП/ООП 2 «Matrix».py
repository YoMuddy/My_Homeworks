class Matrix:
    def __init__(self, data):
        """
        Конструктор: принимает список списков.
        self.data — хранит саму матрицу.
        self.rows и self.cols — хранят её размеры для удобства.
        """
        self.data = data
        self.rows = len(data)
        # Если строк 0, то и столбцов 0, иначе берем длину первой строки
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __str__(self):
        """
        Магический метод для print().
        Обходит каждую строку, превращает числа в текст и склеивает через табуляцию (\t).
        """
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def __eq__(self, other):
        """
        Сравнение двух матриц через ==.
        Сначала проверяем, что размеры совпадают, а потом — сами данные.
        """
        if not isinstance(other, Matrix) or self.size() != other.size():
            return False
        return self.data == other.data

    # --- ИНФОРМАЦИОННЫЕ МЕТОДЫ ---

    def size(self):
        """Возвращает кортеж с размерами (строки, столбцы)."""
        return (self.rows, self.cols)

    def count_elements(self):
        """Считает общее количество ячеек в матрице."""
        return self.rows * self.cols

    def total_sum(self):
        """Считает сумму абсолютно всех чисел в матрице."""
        return sum(sum(row) for row in self.data)

    # --- СИНИЕ МЕТОДЫ (Возвращают новый объект Matrix) ---

    def __add__(self, other):
        """Сложение: берет число из [i][j] первой матрицы и прибавляет число из [i][j] второй."""
        if self.size() != other.size():
            raise ValueError("Матрицы должны быть одинаковых размерностей")

        new_data = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(new_data)

    def __sub__(self, other):
        """Вычитание: работает так же, как сложение, но с минусом."""
        if self.size() != other.size():
            raise ValueError("Матрицы должны быть одинаковых размерностей")

        new_data = [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(new_data)

    def multiply_by_number(self, num):
        """Умножение каждого элемента матрицы на переданное число."""
        new_data = [[val * num for val in row] for row in self.data]
        return Matrix(new_data)

    def transpose(self):
        """Транспонирование: меняет строки и столбцы местами (индексы i и j)."""
        new_data = [
            [self.data[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ]
        return Matrix(new_data)

    def replace_negatives(self):
        """Если число меньше 0, заменяет его на 0 с помощью функции max()."""
        new_data = [[max(0, val) for val in row] for row in self.data]
        return Matrix(new_data)

    # --- ЗЕЛЕНЫЕ МЕТОДЫ (Методы класса @classmethod) ---

    @classmethod
    def eye(cls, m, n):
        """Создает матрицу, где 1 стоят только там, где номер строки равен номеру столбца."""
        data = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        return cls(data)

    @classmethod
    def zeros(cls, m, n):
        """Заполняет сетку размером m на n нулями."""
        data = [[0 for _ in range(n)] for _ in range(m)]
        return cls(data)

    @classmethod
    def diagonal(cls, diag_list):
        """Создает квадратную матрицу, расставляя числа из списка по главной диагонали."""
        n = len(diag_list)
        data = [[diag_list[i] if i == j else 0 for j in range(n)] for i in range(n)]
        return cls(data)


# --- ПРИМЕР РАБОТЫ ---
m = Matrix([[-1, 3], [0, 1], [-2, 2]])
print(f"Исходная матрица:\n{m}")

# Сложение с самой собой
m_sum = m + m
print(f"\nСумма m + m:\n{m_sum}")

# Использование метода класса
diag = Matrix.diagonal([10, 20, 30])
print(f"\nДиагональная матрица:\n{diag}")
