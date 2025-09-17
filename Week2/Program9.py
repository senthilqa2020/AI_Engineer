# Program 9: Bank Account System with OOPs

class BankAccount:
    def __init__(self, account_holder: str, balance: float, account_type: str):
        self.account_holder = account_holder
        self.balance = balance
        self.account_type = account_type

    def deposit(self, amount: float) -> None:
        """Increase balance by the given amount."""
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}")
        else:
            print("Deposit amount must be positive!")

    def withdraw(self, amount: float) -> None:
        """Decrease balance if sufficient funds are available."""
        if amount <= 0:
            print("Withdrawal amount must be positive!")
        elif amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance -= amount
            print(f"Withdrew: {amount}")

    def display_balance(self) -> None:
        """Display account details and current balance."""
        print("\n=== Account Details ===")
        print(f"Account Holder: {self.account_holder}")
        print(f"Account Type  : {self.account_type}")
        print(f"Balance       : {self.balance:.2f}")
        print("=======================\n")


if __name__ == "__main__":
    # Create two accounts
    account1 = BankAccount("Aarav Kumar", 5000.0, "Savings")
    account2 = BankAccount("Diya Sharma", 10000.0, "Current")

    # Perform operations on account1
    account1.display_balance()
    account1.deposit(1500)
    account1.display_balance()
    account1.withdraw(2000)
    account1.display_balance()
    account1.withdraw(6000)  # should trigger "Insufficient balance"

    # Perform operations on account2
    account2.display_balance()
    account2.deposit(2500)
    account2.display_balance()
    account2.withdraw(12000)  # should trigger "Insufficient balance"
    account2.withdraw(5000)
    account2.display_balance()
