from django.conf.urls import url, include
from mgpAPI.views.product import ProductListReportCost,ProductListReportQuantity

urlpatterns = [
    url(r'^quantity/$', ProductListReportQuantity.as_view()),
    url(r'^cost/$', ProductListReportCost.as_view()),
]
