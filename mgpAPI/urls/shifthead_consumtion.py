from django.conf.urls import url, include
from mgpAPI.views.shifthead_consumtion import ShiftHeadConsumptionList

urlpatterns = [
    url(r'^$', ShiftHeadConsumptionList.as_view()),
]
