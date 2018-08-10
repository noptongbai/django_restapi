from django.conf.urls import url, include
from mgpAPI.views.input_transaction import InputTransactionDetail,InputTransactionList
from  mgpAPI.views.input_line_transaction import InputLineTransactionList

urlpatterns = [
    url(r'^$', InputTransactionList.as_view()),
    url(r'^input_line/$',InputLineTransactionList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', InputTransactionDetail.as_view()),
]
