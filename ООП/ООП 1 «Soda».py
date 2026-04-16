class Soda:
    def __init__(self,additive=None):
        if isinstance(additive,str) and additive.strip():
            self.additive = additive
        else:
            self.additive = None
    def show_my_drink(self):
        if self.additive:
            print(f"Газировка и {self.additive}")
        else:
            print(f"Обычная Газировка")

drink1=Soda("Банан")
drink1.show_my_drink()

drink2=Soda()
drink2.show_my_drink()

drink3=Soda("")
drink3.show_my_drink()
