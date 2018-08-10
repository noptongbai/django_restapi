from django.conf.urls import url, include
from mgpAPI.views.outage_extend import OutageExtendViews
from mgpAPI.views.powergeneration_extend import PowerExtendViews
from mgpAPI.views.consumtion_extend import ConsumtionExtendViews
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'outage', OutageExtendViews, base_name='outage')
router.register(r'power', PowerExtendViews, base_name='power')
router.register(r'consumption', ConsumtionExtendViews, base_name='consumption')
urlpatterns = router.urls