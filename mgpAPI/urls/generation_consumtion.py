from django.conf.urls import url, include
from mgpAPI.views.generation_consumtion import ShiftHeadConsumptionList

urlpatterns = [
    url(r'^$', ShiftHeadConsumptionList.as_view()),
]
