from django.conf.urls import url
from mgpAPI.views.outage_consumtion import ReportOutageConsumptionList, ReportOutagePlannedConsumptionList, \
    ReportOutageUnplannedConsumptionList, ReportOutageVariabilityConsumptionList,OutageDetail

urlpatterns = [
    url(r'^all/$', ReportOutageConsumptionList.as_view()),
    url(r'^variability/$', ReportOutageVariabilityConsumptionList.as_view()),
    url(r'^planned/$', ReportOutagePlannedConsumptionList.as_view()),
    url(r'^unplanned/$', ReportOutageUnplannedConsumptionList.as_view()),
]
