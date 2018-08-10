from django.conf.urls import url, include
from mgpAPI.views.erp import SyncErpView, SyncPoView, SyncInputView, SyncToErpInput

urlpatterns = [
    url(r'^sync_erp/$', SyncErpView.as_view()),
    url(r'^sync_po/$', SyncPoView.as_view()),
    url(r'^sync_input/$', SyncInputView.as_view()),
    url(r'^sync_to_erp_input/$', SyncToErpInput.as_view()),
]
