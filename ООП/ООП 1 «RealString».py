class RealString:
    def __init__(self,string):
        self.string = str(string)
    def __len__(self):
        return len(self.string)
    def __eq__(self, other):
        return len(self) == len(other)
    def __lt__(self, other):
        return len(self) < len(other)
    def __le__(self, other):
        return len(self) <= len(other)
    def __gt__(self, other):
        return len(self) > len(other)
    def __ge__(self, other):
        return len(self) >= len(other)

apple = RealString("apple")
apple1 = "Яблоко"

print(apple < apple1)
print(apple == "apple1")
