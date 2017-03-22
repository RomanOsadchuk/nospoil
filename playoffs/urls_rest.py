from django.conf.urls import url
from .views import empty_grid, PlayoffList, PlayoffDetail


urlpatterns = [
    url(r'^empty-grid/$', empty_grid, name='empty-grid'),
    url(r'^playoff/$', PlayoffList.as_view(), name='playoff-list'),
    url(r'^playoff/(?P<pk>[0-9]+)/$',
    	PlayoffDetail.as_view(),
    	name='playoff-detail'),
]
