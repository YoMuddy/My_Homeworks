class GameCharacter:
    def __init__(self, name, health, level):
        self.name = name
        self.health = health
        self.level = level

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value > 100:
            self.__health = 100
        elif value < 0:
            self.__health = 0
        else:
            self.__health = value

    def _level_up(self):
        self.level += 1
        print(f"Уровень персонажа {self.name} повышен до {self.level}!")

    def attack(self, other_character):
        print(f"{self.name} атакует {other_character.name}")
        other_character.health -= 10

    @classmethod
    def create_starter(cls, name):
        return cls(name, 100, 1)

    @staticmethod
    def get_stronger(char1, char2):
        if char1.level > char2.level:
            return char1
        elif char2.level > char1.level:
            return char2
        else:
            return "Уровни равны"

    def __str__(self):
        return f"Персонаж: {self.name}, HP: {self.health}, Level: {self.level}"

hero = GameCharacter.create_starter("Воин")
enemy = GameCharacter("Орк", 150, 2)

hero.attack(enemy)
print(f"Здоровье Орка после атаки: {enemy.health}")

stronger = GameCharacter.get_stronger(hero, enemy)
if isinstance(stronger, GameCharacter):
    print(f"Кто сильнее: {stronger.name}")
else:
    print(stronger)
hero._level_up()
