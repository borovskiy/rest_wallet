from rest_framework import serializers
from .models import Wallet, TransactionsWallet


class WalletSerializer(serializers.ModelSerializer):
    wallet_balance = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'name_wallet', 'wallet_balance']


class OperationWalletSerializer(serializers.ModelSerializer):
    date_operations = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = TransactionsWallet
        fields = ['id', 'wallet', 'operation', 'comment', 'date_operations']
