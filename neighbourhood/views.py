from django.http import HttpResponse, JsonResponse
from django.template import loader
from models import *
from django.shortcuts import render
import json

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

def getchartdata(request, house_id):
    house = House.objects.get(id=house_id)

    df_energy = house.get_total_energy()  # Dataframe
    print df_energy.head(100)
    data = dict()  # data = {}
    data["timeseries"] = []  # data = {"timeseries": []}
    print json.dumps(data)

    for idx in df_energy.index:
        #print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy.ix[idx,"Energieverbruik"]}
        data["timeseries"].append(v_dict)
        #print json.dumps(data)
    return JsonResponse(data)

def getchartdata_room(request, room_id):
    room = Room.objects.get(id=room_id)

    df_energy = room.get_total_energy()  # Dataframe
    print df_energy.head(100)
    data = dict()  # data = {}
    data["timeseries"] = []  # data = {"timeseries": []}
    print json.dumps(data)

    for idx in df_energy.index:
        #print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy.ix[idx,"Energieverbruik"]}
        data["timeseries"].append(v_dict)
        #print json.dumps(data)
    return JsonResponse(data)

def chartdata_comparison(request, house_id_1, house_id_2):
    house1 = House.objects.get(id=house_id_1)
    house2 = House.objects.get(id=house_id_2)

    df_energy1 = house1.get_total_energy()  # Dataframe
    df_energy2 = house2.get_total_energy()  # Dataframe
    data = dict()  # data = {}
    data["first_house"] = []  # data = {"timeseries": []}
    data["second_house"] = []  # data = {"timeseries": []}
    print json.dumps(data)

    for idx in df_energy1.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy1.ix[idx, "Energieverbruik"]}
        data["first_house"].append(v_dict)

    for idx in df_energy2.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy2.ix[idx, "Energieverbruik"]}
        data["second_house"].append(v_dict)
        # print json.dumps(data)
    return JsonResponse(data)

def chartdata_comparisonprice(request, house_id_1, house_id_2):
    house1 = House.objects.get(id=house_id_1)
    house2 = House.objects.get(id=house_id_2)

    df_energy1 = house1.get_total_price()  # Dataframe
    df_energy2 = house2.get_total_price()  # Dataframe
    data = dict()  # data = {}
    data["first_house"] = []  # data = {"timeseries": []}
    data["second_house"] = []  # data = {"timeseries": []}
    print json.dumps(data)

    for idx in df_energy1.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy1.ix[idx, "Price"]}
        data["first_house"].append(v_dict)

    for idx in df_energy2.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy2.ix[idx, "Price"]}
        data["second_house"].append(v_dict)
        # print json.dumps(data)
    return JsonResponse(data)

def vergelijking(request):
    template = loader.get_template('neighbourhood/vergelijking.html')

    slim_huis = House.objects.get(id= 1)
    dom_huis = House.objects.get(id= 2)
    context = {"slim_huis": slim_huis, "dom_huis": dom_huis, "winst": dom_huis.kosten - slim_huis.kosten}
    return TemplateResponse(request,template,context)

def gettotalprice(request,house_id):

    house = House.objects.get(id=house_id)

    df_energy = house.get_total_price()  # Dataframe
    print df_energy.head(5)

    data = dict()  # data = {}
    data["timeseries"] = []  # data = {"timeseries": []}
    print json.dumps(data)

    for idx in df_energy.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy.ix[idx, "Price"]}
        data["timeseries"].append(v_dict)
        # print json.dumps(data)
    return JsonResponse(data)

def gettotalonlyprice(request,house_id):

    house = House.objects.get(id=house_id)
    df_energy = house.get_total_onlyprice()  # Dataframe
    print df_energy.head(5)

    data = dict()  # data = {}
    data["timeseries"] = []  # data = {"timeseries": []}
    print json.dumps(data)

    for idx in df_energy.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy.ix[idx, "Price"]}
        data["timeseries"].append(v_dict)
        # print json.dumps(data)
    return JsonResponse(data)

def chartdata_comparisononlyprice(request, house_id_1, house_id_2):
    house1 = House.objects.get(id=house_id_1)
    house2 = House.objects.get(id=house_id_2)

    df_energy1 = house1.get_total_onlyprice()  # Dataframe
    df_energy2 = house2.get_total_onlyprice() # Dataframe
    data = dict()  # data = {}
    data["first_house"] = []  # data = {"timeseries": []}
    data["second_house"] = []  # data = {"timeseries": []}
    print json.dumps(data)

    for idx in df_energy1.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy1.ix[idx, "Price"]}
        data["first_house"].append(v_dict)

    for idx in df_energy2.index:
        # print idx  # The index of the row => Tijdstap
        v_dict = {"x": datetime.strftime(idx, "%Y-%m-%d %H:%M"), "y": df_energy2.ix[idx, "Price"]}
        data["second_house"].append(v_dict)
        # print json.dumps(data)
    return JsonResponse(data)
