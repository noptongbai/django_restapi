from django.conf.urls import url, include
from mgpAPI.views.preference import PreferenceDetail, PreferenceList

urlpatterns = [
    url(r'^$', PreferenceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', PreferenceDetail.as_view()),
]
