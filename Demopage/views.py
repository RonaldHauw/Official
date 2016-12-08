from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from models import House,Room
from Demopage import *
from Index import *
from neighbourhood import *



def Demo_homepage(request):
    template = loader.get_template('demo/demo_homepage.html')
    return HttpResponse(template.render(request))

def contact(request):
    template = loader.get_template('demo/contact_page.html')
    return HttpResponse(template.render(request))

def demo_uitleg(request):
    template = loader.get_template('demo/Demo_uitleg.html')
    return HttpResponse(template.render(request))

def Root(request):
    template = loader.get_template('Index.html')
    return HttpResponse(template.render(request))

def user_homepage(request):
    template = loader.get_template('neighbourhood/indexneighbourhood.html')
    return HttpResponse(template.render(request))


def centralcontrol(request):
    template = loader.get_template('neighbourhood/Centralcontrol.html')
    return HttpResponse(template.render(request))



