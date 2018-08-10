from django.conf.urls import url, include
from mgpAPI.views.fuelhead_consumtion import FuelHeadConsumptionList

urlpatterns = [
    url(r'^$', FuelHeadConsumptionList.as_view()),
]
