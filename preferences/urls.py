from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.PreferencesView.as_view(), name='PreferencesViews'),

]
