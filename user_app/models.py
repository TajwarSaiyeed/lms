from django.db import models
from django.contrib.auth.models import User


class UserLMSAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    initial_deposit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username