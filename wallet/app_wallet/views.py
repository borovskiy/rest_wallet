from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Wallet, TransactionsWallet
from .serializers import WalletSerializer, OperationWalletSerializer


class ListWalletUser(ViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet

    def list(self, request):
        wallets = Wallet.objects.filter(user='vovka')
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        operations = TransactionsWallet.objects.filter(wallet_id=pk)
        serializer = OperationWalletSerializer(operations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        wallet = Wallet.objects.filter(id=pk).get()
        serialize = WalletSerializer(del_list=['id', 'user', 'wallet_balance'], data=request.data)
        if serialize.is_valid():
            wallet.name_wallet = request.data['name_wallet']
            wallet.save()
            return Response(serialize.data, status.HTTP_201_CREATED)
        return Response(serialize.data, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        object = Wallet.objects.get(id=data['pk'])
        if object:
            object.delete()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


class TransactionsWalletUser(ViewSet):
    def list(self, request):
        operations = TransactionsWallet.objects.filter(wallet__user='vovka').values()
        list_id_operations = [i['id'] for i in operations]
        operations = TransactionsWallet.objects.filter(id__in=list_id_operations)
        serialize = OperationWalletSerializer(operations, many=True)
        return Response(serialize.data)

    def post(self, request):
        serializer = OperationWalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            wallet = Wallet.objects.get(id=serializer['wallet'].value)
            wallet.wallet_balance += serializer['operation'].value
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        object = TransactionsWallet.objects.get(id=data['pk'])
        if object:
            object.delete()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
