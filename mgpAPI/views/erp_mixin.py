from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ViewSetMixin

from mgpAPI.erp_services.syn_all import syncall


class ErpSyncedApiMixedIn(ListModelMixin):
    def list(self, request, *args, **kwargs):
        syncall()
        print "---------------------------------------!!!!!!!!!!!!!!!!!!!!!!"
        return super(ErpSyncedApiMixedIn, self).list(request, *args, **kwargs)
