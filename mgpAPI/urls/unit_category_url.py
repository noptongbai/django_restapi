from django.conf.urls import url, include
from mgpAPI.views.unit_category import UnitCategoryList,UnitCategoryDetail

urlpatterns = [
    url(r'^$', UnitCategoryList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', UnitCategoryDetail.as_view()),
]
