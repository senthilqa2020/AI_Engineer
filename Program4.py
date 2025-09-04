
# ATM Withdrawal: accept an amount and dispense only if it's a multiple of 100

def atm_withdrawal():
    try:
        amount = int(input("Enter withdrawal amount: "))  # read number

        # Valid if positive and divisible by 100
        if amount > 0 and amount % 100 == 0:
            print(f"Dispensing {amount}")
        else:
            print("Invalid amount")
    except ValueError:
        # Handles non-numeric input like 'abc', '12.5', etc.
        print("Invalid amount")

if __name__ == "__main__":
    atm_withdrawal()
