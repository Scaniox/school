
# __ before a variable name is a rule for private variables

class Bank_account():
    def __init__(self, account_name = "Current Account", balance = 200):
        self.__account_name = account_name
        self.__balance = balance


    def get_balance(self):
        return self.__balance


    def set_balance_withdraw(self, value):
        if value < self.__balance :
            self.__balance -= value
            print(f"new balance : {self.__balance}")
        else:
            print("you don't have enough funds!")


account_object = Bank_account()

# main loop
while 1:
    # main method
    print("1. check account balance\n2. withdraw funds")
    menu_option = input()

    # option1 : check balance
    if menu_option == "1":
        print(f"current funds: {account_object.get_balance()}£")

    # option2 : withdraw
    elif menu_option == "2":
        value = int(input("withdraw amount(£): "))
        account_object.set_balance_withdraw(value)

    # incorrect menu choice
    else:
        print("wrong menu choice!\n")
