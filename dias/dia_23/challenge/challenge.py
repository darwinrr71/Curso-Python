class Invoice:
    def __init__(self, total):
        self.total = total

    def is_paid(self):
        return self.total == 0


invoice = Invoice(0)
print(invoice.is_paid())
