class Wallet:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def __apply_bonus(self):
        bonus = self._balance * 0.01
        self._balance += bonus
        print(f"Начислен бонус 1%: {bonus:.2f}")

    def deposit(self, amount):
        """Пополнить кошелёк."""
        if amount > 0:
            self._balance += amount
            print(f"Пополнение на {amount}. Текущий баланс: {self._balance}")
            self.__apply_bonus()
        else:
            print("Сумма пополнения должна быть больше 0")

    def withdraw(self, amount):
        """Снять деньги (если хватает)."""
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"Снято {amount}. Остаток: {self._balance}")
        else:
            print("Недостаточно средств или неверная сумма")

    def transfer_to(self, other_wallet, amount):
        """Перевести деньги другому кошельку."""
        if 0 < amount <= self._balance:
            self._balance -= amount
            other_wallet.deposit(amount)
            print(f"Переведено {amount} пользователю {other_wallet.owner}")
        else:
            print("Ошибка перевода: проверьте баланс")

    @staticmethod
    def wallet_info(wallet):
        print(f"Кошелек владельца: {wallet.owner}, Баланс: {wallet.balance:.2f}")

wallet1 = Wallet("Иван", 1000)
wallet2 = Wallet("Мария", 500)

wallet1.deposit(500)
wallet1.transfer_to(wallet2, 300)

Wallet.wallet_info(wallet1)
Wallet.wallet_info(wallet2)
