from django.conf.urls import url, patterns
from . import views
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url='/myapp/')),
	url(r'^myapp/$', views.index, name='index'),
)