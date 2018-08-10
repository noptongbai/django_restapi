from django.conf.urls import url, include
from mgpAPI.views.report import TaskViewSet
from mgpAPI.views.report_daily import DailyReport

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='tasks')
router.register(r'daily', DailyReport, base_name='daily')
urlpatterns = router.urls
