from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^api/' + settings.VERSION_API + '/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/' + settings.VERSION_API + '/preferences/', include('mgpAPI.urls.preferences_url')),
    url(r'^api/' + settings.VERSION_API + '/products/', include('mgpAPI.urls.product_url')),
    url(r'^api/' + settings.VERSION_API + '/product_categories/', include('mgpAPI.urls.product_category_url')),
    url(r'^api/' + settings.VERSION_API + '/users/', include('mgpAPI.urls.user_url')),
    url(r'^api/' + settings.VERSION_API + '/unit_categories/', include('mgpAPI.urls.unit_category_url')),
    url(r'^api/' + settings.VERSION_API + '/shifts/', include('mgpAPI.urls.shift_url')),
    url(r'^api/' + settings.VERSION_API + '/suppliers/', include('mgpAPI.urls.supplier_url')),
    url(r'^api/' + settings.VERSION_API + '/units/', include('mgpAPI.urls.unit_url')),
    url(r'^api/' + settings.VERSION_API + '/transactions/', include('mgpAPI.urls.transaction_url')),
    url(r'^api/' + settings.VERSION_API + '/transactions/input/', include('mgpAPI.urls.input_transaction')),
    url(r'^api/' + settings.VERSION_API + '/transactions/withdraw/', include('mgpAPI.urls.withdraw_transaction')),
    url(r'^api/' + settings.VERSION_API + '/transactions/return/', include('mgpAPI.urls.return_transaction')),
    url(r'^api/' + settings.VERSION_API + '/transactions/scrap/', include('mgpAPI.urls.scrap_transaction')),
    url(r'^api/' + settings.VERSION_API + '/transactions/adjust/', include('mgpAPI.urls.adjust_transaction')),
    url(r'^api/' + settings.VERSION_API + '/manufacturing/shifthead/', include('mgpAPI.urls.shifthead_consumtion')),
    url(r'^api/' + settings.VERSION_API + '/manufacturing/fuelhead/', include('mgpAPI.urls.fuelhead_consumtion')),
    url(r'^api/' + settings.VERSION_API + '/manufacturing/allhead/', include('mgpAPI.urls.allhead_consumtion')),
    url(r'^api/' + settings.VERSION_API + '/manufacturing/generation/', include('mgpAPI.urls.generation_consumtion')),
    url(r'^api/' + settings.VERSION_API + '/manufacturing/outage/', include('mgpAPI.urls.outage_consumtion')),
    url(r'^api/' + settings.VERSION_API + '/report/product/', include('mgpAPI.urls.report_product_url')),
    url(r'^api/' + settings.VERSION_API + '/report/input_transaction/', include('mgpAPI.urls.report_input_transaction')),
    url(r'^api/' + settings.VERSION_API + '/report/withdraw_transaction/', include('mgpAPI.urls.report_withdraw_transaction')),
    url(r'^api/' + settings.VERSION_API + '/report/power_generation/', include('mgpAPI.urls.report_power_generation')),
    url(r'^api/' + settings.VERSION_API + '/report/outage/', include('mgpAPI.urls.report_outage')),
    url(r'^api/' + settings.VERSION_API + '/report/graph/', include('mgpAPI.urls.report')),
    url(r'^api/' + settings.VERSION_API + '/report/edit/', include('mgpAPI.urls.outage_extend')),
    url(r'^api/' + settings.VERSION_API + '/generation/monitor/', include('mgpAPI.urls.monitor_generation')),
    url(r'^api/' + settings.VERSION_API + '/erp/', include('mgpAPI.urls.erp')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#     # ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)