from django.contrib import admin
from .models import Wallet,TransactionsWallet

admin.site.register(Wallet)
admin.site.register(TransactionsWallet)