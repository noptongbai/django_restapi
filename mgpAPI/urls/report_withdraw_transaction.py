from django.conf.urls import url, include
from mgpAPI.views.withdraw_transaction import WithdrawReportCost, WithdrawReportQuantity
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cost', WithdrawReportCost, base_name='cost')
router.register(r'quantity', WithdrawReportQuantity, base_name='quantity')
urlpatterns = router.urls
