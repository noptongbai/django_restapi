from django.conf.urls import url, include
from mgpAPI.views.return_transaction import ReturnTransactionDetail,ReturnTransactionList

urlpatterns = [
    url(r'^$', ReturnTransactionList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ReturnTransactionDetail.as_view()),
]
