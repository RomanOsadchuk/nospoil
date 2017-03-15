from django.conf.urls import url
import views


app_name = 'playoffs'
urlpatterns = [
    url(r'^$', views.PlayoffIndexView.as_view(), name='index'),
    url(r'^add/$', views.PlayoffCreateView.as_view(), name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.PlayoffUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w-]+)/$', views.PlayoffDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.PlayoffDetailView.as_view()),

    url(r'^api/empty-grid/$', views.empty_grid),
    url(r'^api/playoff/$', views.PlayoffList.as_view()),
    url(r'^api/playoff/(?P<pk>[0-9]+)/$', views.PlayoffDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
