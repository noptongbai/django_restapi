from django.conf.urls import url, include
from mgpAPI.views.transaction import TransactionList

urlpatterns = [
    url(r'^$', TransactionList.as_view()),

]
