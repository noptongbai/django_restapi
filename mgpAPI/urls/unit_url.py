from django.conf.urls import url, include
from mgpAPI.views.unit import UnitList, UnitDetail ,UnitFilterByProduct

urlpatterns = [
    url(r'^$', UnitList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', UnitDetail.as_view()),
    url(r'^filter/$', UnitFilterByProduct.as_view()),
]
