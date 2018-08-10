from django.conf.urls import url, include
from mgpAPI.views.product_category import ProductCategoryList, ProductCategoryDetail

urlpatterns = [
    url(r'^$', ProductCategoryList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ProductCategoryDetail.as_view()),
]
