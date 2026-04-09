class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.status = "в библиотеке"

    def info(self):
        """Выводит информацию о книге."""
        return f"'{self.title}' — {self.author} ({self.year}). Статус: {self.status}"

    def mark_as_taken(self):
        """Меняет статус на «выдана»."""
        self.status = "выдана"

    def mark_as_returned(self):
        """Меняет статус на «в библиотеке»."""
        self.status = "в библиотеке"

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        """Добавляет книги в список."""
        self.books.append(book)

    def remove_book(self, book):
        """Удаляет книгу из библиотеки."""
        if book in self.books:
            self.books.remove(book)

    def find_by_author(self, author):
        """Находит все книги автора."""
        return [b.info() for b in self.books if b.author == author]

    def find_by_year(self, year):
        """Находит все книги указанного года."""
        return [b.info() for b in self.books if b.year == year]

    def available_books(self):
        """Возвращает список всех книг, которые в наличии."""
        return [b.info() for b in self.books if b.status == "в библиотеке"]

    def taken_books(self):
        """Возвращает список всех выданных книг."""
        return [b.info() for b in self.books if b.status == "выдана"]

my_lib = Library("Городская библиотека")

book1 = Book("1984", "Джордж Оруэлл", 1949)
book2 = Book("Ведьмак", "Анджей Сапковский", 1986)

my_lib.add_book(book1)
my_lib.add_book(book2)

book1.mark_as_taken()

print(f"Доступные книги: {my_lib.available_books()}")
print(f"Выданные книги: {my_lib.taken_books()}")
