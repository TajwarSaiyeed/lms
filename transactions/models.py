from django.db import models

from user_app.models import UserLMSAccount

DEPOSIT = 'D'
BORROW = 'B'
REFUND = 'R'

TRANSACTION_TYPES = ( (DEPOSIT, 'Deposit'), (BORROW, 'Borrow'), (REFUND, 'Refund'),)


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    account = models.ForeignKey(UserLMSAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f'{self.amount} - {self.account.user.username}'

    class Meta:
        ordering = ['timestamp']