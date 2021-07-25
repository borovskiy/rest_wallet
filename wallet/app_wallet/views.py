from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions, decorators, response
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet

from .models import Wallet, TransactionsWallet
from .serializers import WalletSerializer, OperationWalletSerializer


class ListWalletUser(ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, req, *args, **kwargs):
        mod = Wallet(user=self.request.user)
        serializer = self.get_serializer(mod, data=req.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TransactionsWalletUser(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             GenericViewSet):
    serializer_class = OperationWalletSerializer
    queryset = TransactionsWallet.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(wallet__user=self.request.user)

    def create(self, req, *args, **kwargs):
        try:
            if Wallet.objects.filter(user=self.request.user).values_list('id').get(id=req.data['wallet']):
                return super().create(req)
        except ObjectDoesNotExist:
            return response.Response(data='HTTP_400_BAD_REQUEST', status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(methods=['get'], detail=True)
    def follow(self, req, pk=None):
        self.queryset = TransactionsWallet.objects.filter(wallet_id=pk, wallet__user=req.user)
        return self.list(req)
