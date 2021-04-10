from django.urls import path, include
from .views import ListWalletUser, TransactionsWalletUser

urlpatterns = [
    path('list_wallet/', ListWalletUser.as_view({'get': 'list'}), name='list_wallets'),
    path('list_wallet/', ListWalletUser.as_view({'post': 'post'}), name='create_wallet'),
    path('list_wallet/<int:pk>', ListWalletUser.as_view({'get': 'retrieve'}), name='list_operations_wallet'),
    path('list_wallet/<int:pk>', ListWalletUser.as_view({'put': 'put'}), name='update_name_wallet'),
    path('list_wallet/', ListWalletUser.as_view({'delete': 'delete'}), name='delete_wallet'),

    path('operation/', TransactionsWalletUser.as_view({'get': 'list'}), name='list_operations'),
    path('operation/', TransactionsWalletUser.as_view({'post': 'post'}), name='create_operation_wallet'),
    path('operation/', TransactionsWalletUser.as_view({'delete': 'delete'}), name='delete_operation_wallet'),

]
