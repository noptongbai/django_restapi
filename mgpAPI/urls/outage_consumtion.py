from django.conf.urls import url, include
from mgpAPI.views.outage_consumtion import OutageConsumptionList

urlpatterns = [
    url(r'^$', OutageConsumptionList.as_view()),
]
