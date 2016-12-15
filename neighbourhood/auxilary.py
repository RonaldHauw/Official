from django.shortcuts import render
# Create your views here.

from multiprocessing import Process
from django.http import HttpResponse
from django.template import loader
from models import *
from helpfunctions import *
from Communicatie import *
import time
import timeit
from neighbourhood.models import *
from django.http import JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
# def change_statusold(request, appliance_id, param_to_change, value):
#     """
#     verandert de opgegeven parameter van een  apparaat in de gegeven value
#     en stuurt dit door via informatie
#     """
#     app = Smart_Devices.objects.get(id=appliance_id)
#     room = app.room
#     house = room.house
#     message = {'%d0%s0%s' % (room.shortcut, param_to_change, value) # dit vult de placeholders in
#     SendInformation('%s:8080' % house.ip, message) # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
#     # de room waarnaar het moet gaan
import threading
from threading import Thread

def change_status(request, device_id, value, roomorhouse, type):
    type = int(type)
    if type == 1:
        device = Smart_Devices.objects.get(id=device_id)
    elif type ==2:
        device = Fridges.objects.get(id=device_id)
    elif type ==3:
        device = Battery.objects.get(id=device_id)
    elif type ==4:
        device = Stupid_Devices.objects.get(id=device_id)
    elif type ==5:
        device = Heating.objects.get(id=device_id)



    house = device.room.house
    ip = house.ip_address
    pintype = device.pin_type

    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie ! nog oppassen want deze kan alleen smart devices aan '
    """
    #initialize()
    message = make_huge_string('change_status',device.room,device.ref_id,'status',value,pintype,'0')
    SendInformation('%s:8080' % ip, message) # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
    # de room waarnaar het moet gaan


    # database updaten
    device.status = value
    device.save()

    #html response
    if roomorhouse == 1:

        template = loader.get_template('neighbourhood/room.html')
        context = {
            'house': Room.objects.get(house=device.room.house, name=device.room.name)
        }
    else:


        template = loader.get_template('neighbourhood/house.html')
        context = {
            'house': House.objects.get(ip_address=house.ip_address)
        }
    return TemplateResponse(request, template, context)
def change_status_smart_2(device_id, value, type):
    type = int(type)
    if type == 1:
        device = Smart_Devices.objects.get(id=device_id)
    elif type ==2:
        device = Fridges.objects.get(id=device_id)
    elif type ==3:
        device = Battery.objects.get(id=device_id)
    elif type ==4:
        device = Stupid_Devices.get(id=device_id)
    elif type ==5:
        device = Heating.object.get(id=device_id)



    house = device.room.house
    ip = house.ip_address
    pintype = device.pin_type


    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie ! nog oppassen want deze kan alleen smart devices aan '
    """
    #initialize()
    message = make_huge_string('change_status',device.room,device.ref_id,'status',value,pintype,'0')
    SendInformation('%s:8080' % ip, message) # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
    # de room waarnaar het moet gaan


    # database updaten
    device.status = value
    device.save()
## als status bij type batterij 60 of 40 is heeft dit betrekking op het geven van energie
# en het stoppen van geven van energie


def initialise(request):
    initialize()
    template = loader.get_template('neighbourhood/init.html')
    return HttpResponse(template.render(request))


tijd_hele_dag = 20




def daytime(request,house_id,roomorhouse):
    p1 = Process(target=central_test)
    p2 = Process(target=centralcontrol)
    p2.start()
    p1.start()
    # huis = House.objects.get(id=house_id)
    #
    #
    # template = loader.get_template('neighbourhood/house.html')
    # context = {
    #     'house': huis
    # }
    # return TemplateResponse(request, template, context)
    template = loader.get_template('neighbourhood/house.html')
    context = {
        'house': House.objects.get(id=house_id)
    }
    return TemplateResponse(request, template, context)








tijd_hele_dag = 240
def centralcontrol(request):
    """
    het programma dat de central control managet
    """

def central_test():
    print('STARTING DAY IN HOUSE 2')


    # initialiseren
    initialize()

    ### continue loop die per stap kijkt naar de tijd, de inputs en dan de database en commando's bijhorden uitvoerd
    starttime = int(timeit.default_timer())

    #### klaarzetten: status van alle apparaten is uit en initialiseren

    while int(timeit.default_timer()) - starttime < tijd_hele_dag:
        ###########
        ###
        ### naar de database kijken en zien welke apparaten er aan staan op dit moment of niet
        ### indien een apparaat volgens de database op dit tijdstip een andere waarde moet hebben
        ### stuurt deze een boodschap naar het betrokken apparaat. Tegelijk
        ###
        ############
        print(int(timeit.default_timer()-starttime))

        curtime = int(timeit.default_timer())
        neig = House.objects.all()
        tijd_96 = time_tijd_hele_dag_naar_96(curtime)
        house = House.objects.get(id=2)
        for room in house.room_set.all():
             ## in de database bij elk te optimaliseren device nog een attribuut geplande tijd? en huidige status##
            for smart_device in room.smart_devices_set.all():


                duration = int(smart_device.duration)
                deadline = smart_device.deadlines_set.all()
                for dead in deadline:
                    if dead - duration - tijd_96 == range(-2,2):
                        smart_device.status = 100
                        smart_device.save()
                        change_status_smart_2(smart_device.ref_id,100,1)
                    if dead -tijd_96 == range(-2,2):
                        smart_device.status = 000
                        smart_device.save()
                        change_status_smart_2(smart_device.ref_id, 000, 1)



            for fridge in room.fridges_set.all():
                duration = int(fridge.duration)
                deadline = fridge.deadlines_set.all()
                for dead in deadline:
                    if dead - duration - tijd_96 == 0:
                        fridge.status = 100
                        fridge.save()
                        change_status_smart_2(fridge.ref_id, 100, 2)
                    if dead - tijd_96 == 0:
                        fridge.status = 000
                        fridge.save()
                        change_status_smart_2(fridge.ref_id, 000, 2)


            for battery in room.battery_set.all():
                 duration = int(battery.duration)
                 deadline = battery.deadlines_set.all()
                 for dead in deadline:

                     if dead - duration - tijd_96 == 0:
                         battery.status = 100
                         battery.save()
                         change_status_smart_2(battery.ref_id, 100, 3)
                     if dead - tijd_96 == 0:
                         battery.status = 000
                         battery.save()
                         change_status_smart_2(battery.ref_id, 000, 3)



            for dumb_device in room.stupid_devices_set.all():
                 duration = int(dumb_device.duration)
                 deadline = dumb_device.deadlines_set.all()
                 for dead in deadline:
                     if dead - duration - tijd_96 == 0:
                         dumb_device.status = 100
                         dumb_device.save()
                         change_status_smart_2(dumb_device.ref_id, 100, 5)
                     if dead - tijd_96 == 0:
                         dumb_device.status = 000
                         dumb_device.save()
                         change_status_smart_2(dumb_device.ref_id, 000, 5)

        ############ Wind en zon bedienen ###########
        if tijd_96 > 12 and tijd_96 < 24:
            change_status_smart_2(7000, 60, 1)
            device = Smart_Devices.objects.get(id=7000)
            device.status = 60
            device.save()
            device = Smart_Devices.objects.get(id=7001)
            device.status = 000
            device.save()
            change_status_smart_2(7001, 000, 1)

        if tijd_96 > 24 and tijd_96 < 50:
            change_status_smart_2(7000, 10, 1)
            device = Smart_Devices.objects.get(id=7000)
            device.status = 10
            device.save()
            device = Smart_Devices.objects.get(id=7001)
            device.status = 100
            device.save()
            change_status_smart_2(7001, 100, 1)

        if tijd_96 > 50 and tijd_96 < 96:
            change_status_smart_2(7000, 80, 1)
            device = Smart_Devices.objects.get(id=7000)
            device.status = 80
            device.save()
            device = Smart_Devices.objects.get(id=7001)
            device.status = 000
            device.save()
            change_status_smart_2(7001, 000, 1)
def centralcontrol(request):
    print('STARTING DAY IN HOUSE 1')

    # initialiseren
    initialize()

    ### continue loop die per stap kijkt naar de tijd, de inputs en dan de database en commando's bijhorden uitvoerd
    starttime = int(timeit.default_timer())

    #### klaarzetten: status van alle apparaten is uit en initialiseren


    while int(timeit.default_timer()) - starttime < tijd_hele_dag:
        ###########
        ###
        ### naar de database kijken en zien welke apparaten er aan staan op dit moment of niet
        ### indien een apparaat volgens de database op dit tijdstip een andere waarde moet hebben
        ### stuurt deze een boodschap naar het betrokken apparaat. Tegelijk
        ###
        ############
        print(int(timeit.default_timer() - starttime))


# def givebattery(request, device_id, value):
#     device = Smart_Device.object.get(id=device_id)
#     house = device.room.house
#     ip = house.ip_address
#
#     """
#     verandert de opgegeven parameter van een  apparaat in de gegeven value
#     en stuurt dit door via informatie
#     """
#
#     message = make_huge_string('change_battery_appliance', device.room, device.ref_id, 'status', value, 'Input', '0')
#     SendInformation('%s:8080' % house_ip,
#                     message)  # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
#     # de room waarnaar het moet gaan
# #
#
#         curtime = int(timeit.default_timer())
#         neig = House.objects.all()
#         tijd_96 = time_tijd_hele_dag_naar_96(curtime)
#         house = House.objects.get(id=1)
#         for room in house.room_set.all():
#             ## in de database bij elk te optimaliseren device nog een attribuut geplande tijd? en huidige status##
#             for smart_device in room.smart_devices_set.all():
#                 whatshould = getoptimaluse(curtime,smart_device)
#                 whatis = smart_device.status
#                 if whatis != whatshould:
#                     change_status_smart_2(smart_device.ref_id,whatshould,1)
#
#
#             for fridge in room.fridges_set.all():
#                 whatshould = getoptimaluse(curtime, fridge)
#                 whatis = fridge.status
#                 if whatis != whatshould:
#                     change_status_smart_2(fridge.ref_id, whatshould, 2)
#
#             for battery in room.battery_set.all():
#                 whatshould = getoptimaluse(curtime, battery)
#                 whatis = battery.status
#                 if whatis != whatshould:
#                     change_status_smart_2(battery.ref_id, whatshould, 3)
#
#             for dumb_device in room.stupid_devices_set.all():
#                 whatshould = getoptimaluse(curtime, dumb_device)
#                 whatis = dumb_device.status
#                 if whatis != whatshould:
#                     change_status_smart_2(dumb_device.ref_id, whatshould, 4)

# def givebattery(request, device_id, value):
#     device = Smart_Device.object.get(id=device_id)
#     house = device.room.house
#     ip = house.ip_address
#
#     """
#     verandert de opgegeven parameter van een  apparaat in de gegeven value
#     en stuurt dit door via informatie
#     """
#
#     message = make_huge_string('change_battery_appliance', device.room, device.ref_id, 'status', value, 'Input', '0', device.pinnumber)
#     SendInformation('%s:8080' % house_ip,
#                     message)  # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
#     # de room waarnaar het moet gaan

def time_tijd_hele_dag_naar_24(curtime):
    fractie = curtime / tijd_hele_dag
    return math.floor(fractie*24)
def time_tijd_hele_dag_naar_96(curtime):
    fractie =curtime/tijd_hele_dag
    return int(fractie*96)
def print_time(curtime):


    return time_tijd_hele_dag_naar_24(curtime)
def give_time_given_96(number):
    """
    Deze functie geeft een waarde weer van 1 tem 96 dat overeenstemt met de tijd op een bepaalde dag.
    Elk getal staat gelijgik aan een kwartier. vb 26 is het 26e kwartier van de dag
    :param time: vb '15:46'
    :return:
    """

    hour = int(number/4)
    minute = (number%4)*15

    return str(hour) + ':' + str(minute)



