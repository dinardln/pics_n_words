from django.http import HttpResponse
from django.template import loader

def index(request):
	template = loader.get_template("myapp/index.html")
	return HttpResponse(template.render());

def second(request):
	template = loader.get_template("myapp/second_page.html")
	return HttpResponse(template.render());
