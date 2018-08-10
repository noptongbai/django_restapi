from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'shifts/$', views.ShiftView.as_view(), name='shifts_views'),

]
