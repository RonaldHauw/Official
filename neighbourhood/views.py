from django.http import HttpResponse, JsonResponse
from django.template import loader
from models import *
from django.shortcuts import render

from django.template.response import TemplateResponse



def house(request,house_id):

    template = loader.get_template('neighbourhood/house.html')
    context = {'house': House.objects.get(id=house_id)}
    #context = {'house': house_id}
    context = {
        'house': House.objects.get(id=house_id)
    }
    return TemplateResponse(request,template,context)

def room(request,id):

    all_rooms = Room.objects.all()
    context = {'room': Room.objects.get(id=id)}
    template = loader.get_template('neighbourhood/room.html')
   # return HttpResponse(template.render(context,request))
    return TemplateResponse(request,template,context)



def indexneighbourhood(request):
    template = loader.get_template('neighbourhood/indexneighbourhood.html')
    return HttpResponse(template.render(request))

def Root(request):
    template = loader.get_template('Index.html')
    return HttpResponse(template.render(request))

def centralcontrol(request):
    template = loader.get_template('neighbourhood/Centralcontrol.html')
    return HttpResponse(template.render(request))

def Demo_homepage(request):
    template = loader.get_template('demo/demo_homepage.html')
    return HttpResponse(template.render(request))



def Root(request):
    template = loader.get_template('Index.html')
    return HttpResponse(template.render(request))

def centralcontrol(request):
    template = loader.get_template('indexcentralcontrol.html')
    return HttpResponse(template.render(request))

def Demo_homepage(request):
    template = loader.get_template('demo/demo_homepage.html')
    return HttpResponse(template.render(request))

def indexcentralcontrol(request):
    template = loader.get_template('neighbourhood/Centralcontrol.html')
    return HttpResponse(template.render(request))

def testinterface(request):
    template = loader.get_template('centralcontrol/testinterface.html')
    return HttpResponse(template.render(request))


def handmatig(request):
    template = loader.get_template('Handmatig.html')
    return HttpResponse(template.render(request))

def getchartdata(request,house_id):
    house = House.objects.get(id=house_id)
    #values = house.get_total_energy()
    data = dict()
    data['timeseries'] = {
                "x": "2013-02-08 09:30",
                "y": 0
            }, {
                "x": "2013-02-08 09:45"  ,
                "y": 5
            }, {
                "x": "2013-02-08 10:00"  ,
                "y": 10
            }, {
                "x": "2013-02-08 10:15"  ,
                "y": 7
            }
    return JsonResponse(data)


def getallcosts(request,house_id):
    house = House.objects.get(id=house_id)
    #values = house.get_total_energy()
    data = dict()
    data['timeseries'] = {
                "x": "2013-02-08 09:33",
                "y": 3
            }, {
                "x": "2013-02-08 09:45"  ,
                "y": 7
            }, {
                "x": "2013-02-08 09:51"  ,
                "y": 10
            }, {
                "x": "2013-02-08 10:55"  ,
                "y": 5
            }
    return JsonResponse(data)


def vergelijking(request):
    template = loader.get_template('neighbourhood/vergelijking.html')
    return HttpResponse(template.render(request))