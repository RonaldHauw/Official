from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from models import House,Room
import Demopage



def Index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))



def ToCentralcontrol(request):
    template = loader.get_template('indexcentralcontrol.html')
    return HttpResponse(template.render(request))