from django.conf.urls import url
from .views import index, create, update, detail


app_name = 'playoffs'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new/$', create, name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', update, name='update'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', detail),
]
