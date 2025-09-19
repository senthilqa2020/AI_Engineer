# Payment Gateway Example using Polymorphism

# Class for Credit Card Payment
class CreditCardPayment:
    def process_payment(self, amount):
        print(f"Processing credit card payment of ${amount}")


# Class for PayPal Payment
class PayPalPayment:
    def process_payment(self, amount):
        print(f"Processing PayPal payment of ${amount}")


# Class for Bank Transfer Payment
class BankTransferPayment:
    def process_payment(self, amount):
        print(f"Processing bank transfer of ${amount}")


# Polymorphic function
def make_payment(payment_method, amount):
    payment_method.process_payment(amount)


# Main section
if __name__ == "__main__":
    # Create objects for each payment method
    credit_card = CreditCardPayment()
    paypal = PayPalPayment()
    bank_transfer = BankTransferPayment()

    # Demonstrate polymorphism
    payments = [credit_card, paypal, bank_transfer]
    amounts = [150, 200, 500]

    for method, amt in zip(payments, amounts):
        make_payment(method, amt)
