
class BankAccount:
    __account_number = None
    __balance = None
    def __init__(self, account_number, balance):
        self.__account_number = account_number
        self.__balance = balance

    def withdrawal(self, amount):
        if amount > self.__balance:
            print("Withdrawal amount is greater then balance:\n Please re-enter amount")
            return
        self.__balance -= amount
        print(f"withdrawal is successfully!\nyou withdraw {amount} from account no: {self.__account_number}")
    def balance_inquiry(self):
        print(f"Your account balance: {self.__balance}")
    def get_balance(self):
        return self.__balance
    def set_balance(self, amount):
        self.__balance = amount
    def get_account_number(self):
        return self.__account_number

class SavingAccount(BankAccount):
    __interest_rate = 4.25

    def __init__(self, account_number, balance):
        super().__init__(account_number, balance)

    def calculate_interest(self):
        total_interest = self.__interest_rate * self.get_balance() / 100
        self.set_balance(self.get_balance() + total_interest)
        print(f"Calculated interest {total_interest}, balance {self.get_balance()}")


class DepositAccount(BankAccount):
    __interest_rate = 8.15

    def __init__(self, account_number, balance):
        BankAccount.__init__(self, account_number, balance)

    def calculate_interest(self):
        total_interest = self.__interest_rate * self.get_balance() / 100
        self.set_balance(self.get_balance() + total_interest)
        print(f"Calculated interest {total_interest}, balance {self.get_balance()}")

savings = SavingAccount("123456", 200)

deposit = DepositAccount("1234567", 200)

savings.balance_inquiry()
savings.calculate_interest()
deposit.calculate_interest()

# print(deposit.account_number)