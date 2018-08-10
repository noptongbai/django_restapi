from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'units_categories/$', views.UnitCategoryView.as_view(), name='units_categories_views'),
    url(r'units/$', views.UnitView.as_view(), name='units_views')
]
