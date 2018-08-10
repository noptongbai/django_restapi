from django.conf.urls import url, include
from mgpAPI.views.scrap_transaction import ScrapTransactionDetail,ScrapTransactionList

urlpatterns = [
    url(r'^$', ScrapTransactionList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ScrapTransactionDetail.as_view()),
]
