from django.conf.urls import url, include
from mgpAPI.views.shift import ShiftList, ShiftDetail

urlpatterns = [
    url(r'^$', ShiftList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ShiftDetail.as_view()),
]
