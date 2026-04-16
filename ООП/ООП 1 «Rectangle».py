class Rectangle:
    def __init__(self,width,height):
        self.width = width
        self.height = height
    def __str__(self):
        return f"Прямоугольник с шириной {self.width} и высотой {self.height}"
    def get_area(self):
        return self.width * self.height
    def get_perimeter(self):
        return 2 * (self.width + self.height)
    @property
    def is_square(self):
        return self.width == self.height

rect = Rectangle(10,5)
print(rect)
print(rect.get_area())
print(rect.get_perimeter())
print(rect.is_square)
