from django.conf.urls import url
import views


app_name = 'playoffs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.update, name='update'),
    url(r'^detail/(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', views.detail, name='detail'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.detail),

    url(r'^api/empty-grid/$', views.empty_grid),
    url(r'^api/playoff/$', views.PlayoffList.as_view()),
    url(r'^api/playoff/(?P<pk>[0-9]+)/$', views.PlayoffDetail.as_view()),
]
