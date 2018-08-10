from django.conf.urls import url, include
from mgpAPI.views.allhead_consumtion import FuelHeadConsumptionList,MonitorConsumptionList

urlpatterns = [
    url(r'^$', FuelHeadConsumptionList.as_view()),
    url(r'^monitor_consumption/$', MonitorConsumptionList.as_view()),
]
