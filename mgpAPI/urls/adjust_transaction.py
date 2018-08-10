from django.conf.urls import url, include
from mgpAPI.views.adjust_transaction import AdjustTransactionDetail,AdjustTransactionList

urlpatterns = [
    url(r'^$', AdjustTransactionList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', AdjustTransactionDetail.as_view()),
]
