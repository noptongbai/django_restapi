from django.conf.urls import url, include
from mgpAPI.views.withdraw_transaction import WithdrawTransactionDetail,WithdrawTransactionList

urlpatterns = [
    url(r'^$', WithdrawTransactionList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', WithdrawTransactionDetail.as_view()),
]
