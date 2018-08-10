from django.conf.urls import url, include
from mgpAPI.views.monitor_all_generation import GenerationConsumptionMonitor, ConsumptionMonitor, OutagenMonitor, \
    GenerationConsumptionMonitorLast
from mgpAPI.views.generation_consumtion import PowerGenerationDetail
from mgpAPI.views.outage_consumtion import OutageDetail

urlpatterns = [
    url(r'^generation/$', GenerationConsumptionMonitor.as_view()),
    url(r'^generation/last/$', GenerationConsumptionMonitorLast.as_view()),
    url(r'^consumption/$', ConsumptionMonitor.as_view()),
    url(r'^outage/$', OutagenMonitor.as_view()),
    url(r'^edit/outage/(?P<pk>[0-9]+)/$', OutageDetail.as_view()),
    url(r'^edit/generation/(?P<pk>[0-9]+)/$', PowerGenerationDetail.as_view()),
    url(r'^delete/consumption/(?P<pk>[0-9]+)/$', PowerGenerationDetail.as_view()),
]
