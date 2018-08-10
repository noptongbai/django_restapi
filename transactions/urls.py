from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'suppliers/$', views.SupplierView.as_view(), name='shifts_views'),

]
