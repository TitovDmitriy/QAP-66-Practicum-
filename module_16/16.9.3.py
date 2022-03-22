# В проекте «Дом питомца» скоро появится новая услуга: электронный кошелек. 
#То есть система будет хранить данные о своих клиентах и об их финансовых операциях.
#
# Вам нужно написать программу, обрабатывающую данные, и на выходе в консоль
# получить следующее: Клиент "Иван Петров". Баланс: 50 руб.

class Wallet():
    def __init__(self, name, surname, balance):
        self. name = name
        self.surname = surname
        self.balance = int(balance)

    def Parameters(self):
       return f"Клиент {self. name} {self. surname}. Баланс: {self.balance} руб."

    
n = Wallet("Иван", "Петров", 50)
print(n.Parameters())

