from django.db import models


class Wallet(models.Model):
    user = models.CharField(max_length=50, verbose_name='Пользователь')
    name_wallet = models.CharField(max_length=50, verbose_name='Имя кошелька')
    wallet_balance = models.FloatField(verbose_name='Баланс кошелька', default=0.0)

    def __str__(self):
        return f'{self.user}-{self.name_wallet}'


class TransactionsWallet(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, verbose_name='Кошелек')
    operation = models.FloatField(max_length=30, verbose_name='Операция', default=0.0)
    comment = models.CharField(max_length=100, verbose_name='Комментарий', blank=True, null=True)
    date_operations = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время операции')

    def __str__(self):
        return f'{self.wallet}:  {self.operation}'
