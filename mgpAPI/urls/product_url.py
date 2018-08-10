from django.conf.urls import url, include
from mgpAPI.views.product import ProductList, ProductDetail

urlpatterns = [
    url(r'^$', ProductList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ProductDetail.as_view()),
]
