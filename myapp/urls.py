from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^$', RedirectView.as_view(url='/myapp/')),
	url(r'^myapp/$', views.index, name='index'),
	url(r'^yourapp/$', views.second, name='second_page'),
]
