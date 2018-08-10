from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'product_categories/$', views.ProductCategoryView.as_view(), name='ProductCategoriesViews'),
    url(r'products/$', views.ProductView.as_view(), name='ProductViews'),

]
