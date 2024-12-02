from payment_processor import PaymentProcessor

class PayPalPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return True