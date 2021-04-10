from rest_framework import serializers
from .models import Wallet, TransactionsWallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id','name_wallet', 'wallet_balance']
    # 'TODO тут по желанию можно убрать баланс кошелька и оставить умолчание.'

    def __init__(self, *args, **kwargs):
        del_list = kwargs.pop('del_list', None)
        super(WalletSerializer, self).__init__(*args, **kwargs)
        if del_list is not None:
            for i in del_list:
                del self.fields[i]


class OperationWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionsWallet
        fields = ['id', 'wallet', 'operation', 'comment']
