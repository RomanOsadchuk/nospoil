from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views import RegistrationView, ProfileView, UserPageView


app_name = 'accounts'
urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', lambda r: logout(r, next_page='/'), name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<username>\w+)/$', UserPageView.as_view(), name='user_page'),
]
