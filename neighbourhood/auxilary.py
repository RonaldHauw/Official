from django.shortcuts import render
from multiprocessing import Process
from django.http import HttpResponse
from django.template import loader
from models import *
from helpfunctions import *
from Communicatie import *
import time
import timeit
from neighbourhood.models import Smart_Devices
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
    p1.start()
    # huis = House.objects.get(id=house_id)
    #
    #
    # template = loader.get_template('neighbourhood/house.html')
    # context = {
    #     'house': huis
    # }
    # return TemplateResponse(request, template, context)

    template = loader.get_template('neighbourhood/indexneighbourhood.html')
    return HttpResponse(template.render(request))






def central_test():
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
        house = House.objects.get(id=2)#### itereren over alle apparaten in dom huis ###
        for room in house.room_set.all():
             ## in de database bij elk te optimaliseren device nog een attribuut geplande tijd? en huidige status##
            for smart_device in room.smart_devices_set.all():


                duration = int(smart_device.duration)
                deadline = smart_device.deadlines.all()

                if deadline - duration - tijd_96 == range(-2,2):
                    smart_device.status = 100
                    smart_device.save()
                    change_status_smart_2(smart_device.ref_id,100,1)
                if deadline -tijd_96 == range(-1,1):
                    smart_device.status = 000
                    smart_device.save()
                    change_status_smart_2(smart_device.ref_id, 000, 1)



            for fridge in room.fridges_set.all():
                duration = int(fridge.duration)
                deadline = int(fridge.deadlines)

                if deadline - duration - tijd_96 == 0:
                    fridge.status = 100
                    fridge.save()
                    change_status_smart_2(fridge.ref_id, 100, 2)
                if deadline - tijd_96 == 0:
                    fridge.status = 000
                    fridge.save()
                    change_status_smart_2(fridge.ref_id, 000, 2)


            for battery in room.battery_set.all():
                 duration = int(battery.duration)
                 deadline = int(battery.deadlines)

                 if deadline - duration - tijd_96 == 0:
                     battery.status = 100
                     battery.save()
                     change_status_smart_2(battery.ref_id, 100, 3)
                 if deadline - tijd_96 == 0:
                     battery.status = 000
                     battery.save()
                     change_status_smart_2(battery.ref_id, 000, 3)



            for dumb_device in room.stupid_devices_set.all():
                 duration = int(dumb_device.duration)
                 deadline = int(dumb_device.deadlines)

                 if deadline - duration - tijd_96 == 0:
                     dumb_device.status = 100
                     dumb_device.save()
                     change_status_smart_2(dumb_device.ref_id, 100, 5)
                 if deadline - tijd_96 == 0:
                     dumb_device.status = 000
                     dumb_device.save()
                     change_status_smart_2(dumb_device.ref_id, 000, 5)







def centralcontrol(request):
    """
    het programma dat de central control managet
    """


    # initialiseren
    initialize()

    ### continue loop die per stap kijkt naar de tijd, de inputs en dan de database en commando's bijhorden uitvoerd
    starttime=timeit.default_timer()

    #### klaarzetten: status van alle apparaten is uit en initialiseren




    while timeit.default_timer() - starttime < tijd_hele_dag:
        ###########
        ###
        ### naar de database kijken en zien welke apparaten er aan staan op dit moment of niet
        ### indien een apparaat volgens de database op dit tijdstip een andere waarde moet hebben
        ### stuurt deze een boodschap naar het betrokken apparaat. Tegelijk
        ###
        ############


        curtime=timeit.default_timer()
        update_clock(curtime)

        price = getprice(curtime)
        solar = getsolar(curtime)
        wind = getwind(curtime)



        neig = House.objects.all()

        for house in neig: #### itereren over alle apparaten ###
            for room in house.room_set.all():
                ## in de database bij elk te optimaliseren device nog een attribuut geplande tijd? en huidige status##
                for smart_device in room.smart_devices_set.all():
                    curplan = getcurplan(smart_device,curtime) ## geeft de status dat het apparaat zou moeten hebben terug
                    curstatus = smart_device.status
                    cur_id = smart_device.ref_id

                    if curplan != curstatus:
                        change_status(request,cur_id,curplan) ### doorsturen naar huisjes
                        smart_device.status = curplan


                for fridge in room.fridges_set.all():
                    curplan = getcurplan(fridge, curtime)  ## geeft de status dat het apparaat zou moeten hebben terug
                    curstatus = fridge.status
                    cur_id = fridge.ref_id

                    if curplan != curstatus:
                        change_status(request, cur_id, curplan)  ### doorsturen naar huisjes
                        fridge.status = curplan

                for battery in room.battery_set.all():
                    curplan = getcurplan(battery,
                                         curtime)  ## geeft de status dat het apparaat zou moeten hebben terug
                    curstatus = battery.status
                    cur_id = battery.ref_id

                    if curplan != curstatus:
                        change_status(request, cur_id, curplan)  ### doorsturen naar huisjes
                        battery.status = curplan

                for heater in room.heating_set.all():
                    curplan = getcurplan(heater,
                                         curtime)  ## geeft de status dat het apparaat zou moeten hebben terug
                    curstatus = heater.status
                    cur_id = heater.ref_id

                    if curplan != curstatus:
                        change_status(request, cur_id, curplan)  ### doorsturen naar huisjes
                        heater.status = curplan

                for dumb_device in room.stupid_devices_set.all():
                    curplan = getcurplan(dumb_device,
                                         curtime)  ## geeft de status dat het apparaat zou moeten hebben terug
                    curstatus = dumb_device.status
                    cur_id = dumb_device.ref_id

                    if curplan != curstatus:
                        change_status(request, cur_id, curplan)  ### doorsturen naar huisjes
                        dumb_device.status = curplan






        #### !!!!!! als een lamp momenteel aangepast moet worden moet dit in de database worden gedaan !!!!! #####
        #### !!!!!! Dit programma gaat gewoon kijken naar het resultaat van de optimalistatie en in functie van de tijd
        ###         De status van de betrokken apparaten aanpassen

def givebattery(request, device_id, value):
    device = Smart_Device.object.get(id=device_id)
    house = device.room.house
    ip = house.ip_address

    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie
    """

    message = make_huge_string('change_battery_appliance', device.room, device.ref_id, 'status', value, 'Input', '0', device.pinnumber)
    SendInformation('%s:8080' % house_ip,
                    message)  # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
    # de room waarnaar het moet gaan


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



