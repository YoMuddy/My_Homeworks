class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        """Добавляет оценку в список."""
        if 1 <= grade <= 12:
            self.grades.append(grade)

    def average_grade(self):
        """Считает средний балл ученика."""
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def info(self):
        """Возвращает строку с данными ученика."""
        return f"Студент: {self.name}, Средний балл: {self.average_grade():.2f}"


class StudyGroup:
    def __init__(self, group_name):
        self.group_name = group_name
        self.students = []

    def add_student(self, student):
        """Добавляет объект класса Student в группу."""
        self.students.append(student)

    def remove_student(self, name):
        """Удаляет студента из списка по имени."""
        self.students = [s for s in self.students if s.name != name]

    def find_best_student(self):
        """Находит студента с самым высоким средним баллом."""
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.average_grade())

    def group_average(self):
        """Считает средний балл всей группы."""
        if not self.students:
            return 0
        total = sum(s.average_grade() for s in self.students)
        return total / len(self.students)

    def list_students(self):
        """Выводит информацию о каждом студенте группы."""
        print(self.group_name)
        for s in self.students:
            print(f"- {s.info()}")

s1 = Student("Иван")
s1.add_grade(5)
s1.add_grade(4)

s2 = Student("Анна")
s2.add_grade(5)
s2.add_grade(5)

my_group = StudyGroup("Программисты-101")
my_group.add_student(s1)
my_group.add_student(s2)

print(f"Лучший в группе: {my_group.find_best_student().name}")
my_group.list_students()
