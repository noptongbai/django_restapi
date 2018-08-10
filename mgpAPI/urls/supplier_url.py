from django.conf.urls import url, include
from mgpAPI.views.supplier import SupplierList, SupplierDetail

urlpatterns = [
    url(r'^$', SupplierList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', SupplierDetail.as_view()),
]
