class TriangleChecker:
    def __init__(self,a,b,c):
        self.sides= [a,b,c]

    def check(self):
        for side in self.sides:
            if not isinstance(side, (int, float)):
                return "Нужно вводить только числа!"

        if any(side <= 0 for side in self.sides):
            return "С отрицательными числами ничего не выйдет!"

        a,b,c = self.sides
        if (a + b > c) and (a + c > b) and (b + c > a):
            return "Можем построить треугольник"
        else:
            return "Из этого треугольник не получится"

checker1 = TriangleChecker(10,10,10)
print(f"10, 10, 10: {checker1.check()}")

checker2 = TriangleChecker(1,1,10)
print(f"1, 1, 10: {checker2.check()}")

checker3 = TriangleChecker(-5,5,5)
print(f"-5, 5, 5: {checker3.check()}")

checker4 = TriangleChecker("10",5,5)
print(f"10, 5, 5: {checker4.check()}")
