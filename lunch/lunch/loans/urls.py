# loans/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loan_list, name='loan_list'),
    url(r'^new/$', views.loan_create, name='loan_create'),
    url(r'^(?P<pk>\d+)/$', views.loan_detail, name='loan_detail'),
    url(r'^(?P<pk>\d+)/update/$', views.loan_update, name='loan_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.loan_delete, name='loan_delete'),
    url(r'^utk/$', views.utk_search, name='utk_search'),
    url(r'^export/$', views.export_xlsx, name='export_xlsx'),
    #url(r'^utkvalue$', views.utk_value),
]
