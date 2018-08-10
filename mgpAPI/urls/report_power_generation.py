from django.conf.urls import url
from mgpAPI.views.generation_consumtion import ReportPowerSteam, ReportPowerGenerationLast, ReportPowerGeneration, \
    ReportPowerExport, \
    PowerGenerationDetail

urlpatterns = [
    url(r'^steam/$', ReportPowerSteam.as_view()),
    url(r'^generation/$', ReportPowerGeneration.as_view()),
    url(r'^generation/last/$', ReportPowerGenerationLast.as_view()),
    url(r'^export/$', ReportPowerExport.as_view()),
]
