from django.conf.urls import url, include
from mgpAPI.views.input_transaction import InputReportCost, InputReportQuantity
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cost', InputReportCost, base_name='cost')
router.register(r'quantity', InputReportQuantity, base_name='quantity')
urlpatterns = router.urls
