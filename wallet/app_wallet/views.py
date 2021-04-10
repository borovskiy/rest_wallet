from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Wallet, TransactionsWallet
from .serializers import WalletSerializer, OperationWalletSerializer


class ListWalletUser(ViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet

    # список кошельков
    def list(self, request):
        wallets = Wallet.objects.filter(user_id=request.user.id)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

    # список операция одного кошелька
    def retrieve(self, request, pk):
        operations = TransactionsWallet.objects.filter(wallet_id=pk)
        serializer = OperationWalletSerializer(operations, many=True)
        return Response(serializer.data)

    # создание кошелька
    def post(self, request):
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)

    # изменение имени кошелька
    def put(self, request, pk):
        wallet = Wallet.objects.filter(id=pk).get()
        serialize = WalletSerializer(del_list=['id', 'wallet_balance'], data=request.data)
        if serialize.is_valid():
            wallet.name_wallet = request.data['name_wallet']
            wallet.save()
            return Response(serialize.data, status.HTTP_201_CREATED)
        return Response(serialize.data, status.HTTP_400_BAD_REQUEST)

    # удаление кошелька
    def delete(self, request):
        data = request.data
        object = Wallet.objects.get(id=data['pk'])
        if object:
            object.delete()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


class TransactionsWalletUser(ViewSet):

    # список всех транзакций
    def list(self, request):
        operations = TransactionsWallet.objects.filter(wallet__user=request.user.id).values()
        list_id_operations = [i['id'] for i in operations]
        operations = TransactionsWallet.objects.filter(id__in=list_id_operations)
        serialize = OperationWalletSerializer(operations, many=True)
        return Response(serialize.data)

    # создание транзакции и действие в кошельке
    def post(self, request):
        serializer = OperationWalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            wallet = Wallet.objects.get(id=serializer['wallet'].value)
            wallet.wallet_balance += serializer['operation'].value
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # удаление транзанции
    def delete(self, request):
        data = request.data
        object = TransactionsWallet.objects.get(id=data['pk'])
        if object:
            object.delete()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
