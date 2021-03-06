from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


home_page_view = TemplateView.as_view(template_name='home_page.html')

urlpatterns = [
    url(r'^$', home_page_view, name='home_page'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^playoffs/', include('playoffs.urls')),
    url(r'^api/', include('playoffs.urls_rest')),
    url(r'^api-auth/', include('rest_framework.urls')),
]
