from django.urls import path, include
from rest_framework import routers
from .views import ListWalletUser, TransactionsWalletUser

router = routers.SimpleRouter()
router.register('wallets', ListWalletUser)
router.register('operations', TransactionsWalletUser)
urlpatterns = [] + router.urls
