from django.conf.urls import url
from .views import PlayoffIndexView, PlayoffDetailView, PlayoffCreateView, PlayoffUpdateView


app_name = 'playoffs'
urlpatterns = [
    url(r'^$', PlayoffIndexView.as_view(), name='index'),
    url(r'^add/$', PlayoffCreateView.as_view(), name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', PlayoffUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', PlayoffDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', PlayoffDetailView.as_view()),
]
