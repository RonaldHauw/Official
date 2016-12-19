from django.shortcuts import render
# Create your views here.
data = []
data2 = []
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
import sys
sys.path.append("..")
from models import *
from auxilary import *
import csv
import math
import Communicatie
import models
import helpfunctions
import threading
from threading import Thread




tijd_hele_dag = 40







def central_test():
    data.append("-STARTING DAY IN HOUSE 2")


    starttime = int(timeit.default_timer())
    data.append("-initialiseren")
    helpfunctions.initialize()
    data.append("-initialiseren klaar")


    while int(timeit.default_timer() - starttime )< tijd_hele_dag:



        curtime = int(timeit.default_timer()-starttime)
        tijd_96 = int(time_tijd_hele_dag_naar_96(curtime))
        house = models.House.objects.get(id=2)

        data.append("--het is nu: %s zo laat" % str(tijd_96))

        for room in house.room_set.all():
            data.append("--nakijken in kamer %s" % room.name)
            for smart_device in room.smart_devices_set.all():
                data.append("---devevices nakijken: nu %s" %smart_device.ref_id)


                duration = int(smart_device.duration)
                dead = smart_device.deadlin
                data.append("deadline gevonden %s" % dead)
                #deadline = smart_device.deadlines.objects.all()
                # data.append("deadlines gevonden... %s" % deadlines)
                # data.append("---duurtijd apparaat: %s " % duration)
                # for dead in deadline:
                #     data.append("----gevonden deadline: %s  ---- trigger: %s" % (dead.timestamp, dead.timestamp - duration -tijd_96))
                #
                #     if dead.timestamp - duration - tijd_96 == 0:
                #         data.append("-!!!!!!!!!!!!!!!!!!!!!!!!----Deadline wordt actief:----------------------------")
                #         smart_device.status = 100
                #         smart_device.save()
                #         change_status_smart_2(smart_device.ref_id,100,1)
                #         data.append("-----Activeren van apparaat: %s" % smart_device.ref_id)
                #     if dead.timestamp -tijd_96 == 0:
                #         data.append("-----Deadline wordt inactief: uitschakelen apparaat ")
                #         smart_device.status = 000
                #         smart_device.save()
                #         change_status_smart_2(smart_device.ref_id, 000, 1)

                data.append("wtf scheelt er")
                if int(dead) - int(duration) - int(tijd_96) == 0:
                     data.append("-!!!!!!!!!!!!!!!!!!!!!!!!----Deadline wordt actief:----------------------------")
                     smart_device.status = 100
                     smart_device.save()
                     data.append("probleem met data als dit niet komt: reffer %s" % smart_device.ref_id)
                     change_status_smart_2(smart_device.ref_id,100,1)
                     data.append("probleem met change status Z")
                     data2.append("Ik verander nu apparaat %s zijn status naar %s omdat de deadline %s behaald moet worden, en het is nu al %s kwartier laat" % (smart_device.name, 100, dead, tijd_96))
                     data.append("-----Activeren van apparaat: %s" % smart_device.ref_id)
                if int(dead) -int(tijd_96) == 0:
                     data.append("-----Deadline wordt inactief: uitschakelen apparaat------------------------------- ")
                     smart_device.status = 000
                     smart_device.save()
                     change_status_smart_2(smart_device.ref_id, 000, 1)
                data.append("checkpoint")

            for fridge in room.fridges_set.all():
                data.append("-- devevices nakijken: nu %s" %fridge.ref_id)




            for battery in room.battery_set.all():
                data.append("-- devevices nakijken: nu %s" % battery.ref_id)





            for dumb_device in room.stupid_devices_set.all():
                data.append("-- devevices nakijken: nu %s , naam is %s, normale duur is %s, deadline is %s" % (dumb_device.ref_id, dumb_device.name, dumb_device.duration,dumb_device.deadlin))
                duration = int(dumb_device.duration)
                dead = int(dumb_device.deadlin)
                if int(dead) - duration - tijd_96 == 0:
                    data.append("-!!!!!!!!!!!!!!!!!!!!!!!!----Deadline wordt actief:----------------------------")
                    dumb_device.status = 100
                    dumb_device.save()
                    data.append("probleem met data als dit niet komt: reffer %s" % dumb_device.ref_id)
                    data2.append( "Ik verander nu apparaat %s zijn status naar %s omdat de deadline %s behaald moet worden, en het is nu al %s kwartier laat" % (
                        dumb_device.name, 100, dead, tijd_96))

                    change_status_smart_2(dumb_device.ref_id, 100, 1)
                    data.append("probleem met change status Z")
                    data.append("-----Activeren van apparaat: %s" % dumb_device.ref_id)
                if int(dead) - tijd_96 == 0:
                    data.append("-----Deadline wordt inactief: uitschakelen apparaat------------------------------- ")
                    dumb_device.status = 000
                    dumb_device.save()
                    change_status_smart_2(dumb_device.ref_id, 000, 1)




        ############ Wind en zon bedienen ###########
        if tijd_96 > 12 and tijd_96 < 24:
            change_status_smart_2(7000, 60, 1)
            device = models.Smart_Devices.objects.get(ref_id=7000)
            device.status = 60
            device.save()
            device = models.Smart_Devices.objects.get(ref_id=7001)
            device.status = 000
            device.save()
            change_status_smart_2(7001, 000, 1)

        if tijd_96 > 24 and tijd_96 < 50:
            change_status_smart_2(7000, 10, 1)
            device = models.Smart_Devices.objects.get(ref_id=7000)
            device.status = 10
            device.save()
            device = models.Smart_Devices.objects.get(ref_id=7001)
            device.status = 100
            device.save()
            change_status_smart_2(7001, 100, 1)

        if tijd_96 > 50 and tijd_96 < 96:
            change_status_smart_2(7000, 80, 1)
            device = models.Smart_Devices.objects.get(ref_id=7000)
            device.status = 80
            device.save()
            device = models.Smart_Devices.objects.get(ref_id=7001)
            device.status = 000
            device.save()
            change_status_smart_2(7001, 000, 1)
    data.append("DAG IS AFGELOPEN !!!!!")

def centralcontrol():
    print('STARTING DAY IN HOUSE 1')

    initialize()

    starttime = int(timeit.default_timer())



def init_auxilary(request):
    data=[]
    data2=[]
    global data
    global data2
    template = loader.get_template('neighbourhood/indexneighbourhood.html')
    return HttpResponse(template.render(request))

def change_status(request, device_id, value, roomorhouse, type):
    data.append("changing status of device %s of type %s to value %s" % (device_id, value, type))
    type = int(type)
    if type == 1:
        device = models.Smart_Devices.objects.get(id=device_id)
    elif type == 2:
        device = models.Fridges.objects.get(id=device_id)
    elif type == 3:
        device = models.Battery.objects.get(id=device_id)
    elif type == 4:
        device = models.Stupid_Devices.objects.get(id=device_id)
    elif type == 5:
        device = models.Heating.objects.get(id=device_id)
        house = device.House
        ip = house.ip_address
        pintype = "output"
        room = "ihavenoroom"

    if type != 5:
        house = device.room.house
        ip = house.ip_address
        pintype = device.pin_type
        room = device.room

    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie ! nog oppassen want deze kan alleen smart devices aan '
    """
    # initialize()
    message = make_huge_string('change_status', room, device.ref_id, 'status', value, str(pintype), '0')
    if not testing:
        Communicatie.SendInformation('%s:8080' % ip, message)

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
            'house': models.House.objects.get(ip_address=house.ip_address)
        }
    return TemplateResponse(request, template, context)

def change_status_smart_2(device_id, value, type):
    data.append("in change status 2")
    type = int(type)
    data.append("%s" %type)
    if type == 1:
        data.append("in right type")
        device = models.Smart_Devices.objects.get(ref_id=device_id) # hier zit een fout !!!
        data.append("got the device")
    elif type ==2:
        device = models.Fridges.objects.get(ref_id=device_id)
    elif type ==3:
        device = models.Battery.objects.get(ref_id=device_id)
    elif type ==4:
        device = models.Stupid_Devices.get(ref_id=device_id)
    elif type == 5:
        device = models.Heating.objects.get(ref_id=device_id)
        house = device.house
        ip = house.ip_address
        pintype = "output"
        room = "ihavenoroom"
    data.append("able to get object")

    if type != 5:
        house = device.room.house
        ip = house.ip_address
        pintype = device.pin_type
        room = device.room




    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie ! nog oppassen want deze kan alleen smart devices aan '
    """
    #initialize()
    message = make_huge_string('change_status',room,device.ref_id,'status',value,pintype,'0')
    if not testing:
        SendInformation('%s:8080' % ip, message)


    # database updaten
    device.status = value
    device.save()

def initialise(request):
    helpfunctions.initialize()
    template = loader.get_template('neighbourhood/init.html')
    return HttpResponse(template.render(request))

def daytime(request):
    data.append("STARTING DAYTIME")
    p1 = Thread(target=central_test)
    p2 = Thread(target=centralcontrol)



    p1.start()
    p2.start()
    data.append("both processes running, daytime returns house.html")
    # huis = House.objects.get(id=house_id)
    #
    #
    # template = loader.get_template('neighbourhood/house.html')
    # context = {
    #     'house': huis
    # }
    # return TemplateResponse(request, template, context)
    template = loader.get_template('neighbourhood/vergelijking.html')
    return HttpResponse(template.render(request))

def time_tijd_hele_dag_naar_96(curtime):
    fractie = curtime*tijd_hele_dag**-1
    return int(fractie*96)


def change_status_2(device_id, value, type):
    data.append("changing status of device %s of type %s to value %s" % (device_id, value, type))
    type = int(type)
    if type == 1:
        device = models.Smart_Devices.objects.get(id=device_id)
    elif type ==2:
        device = models.Fridges.objects.get(id=device_id)
    elif type ==3:
        device = models.Battery.objects.get(id=device_id)
    elif type ==4:
        device = models.Stupid_Devices.objects.get(id=device_id)
    elif type ==5:
        device = models.Heating.objects.get(id=device_id)
        house = device.house
        ip = house.ip_address
        pintype = "output"
        room = "ihavenoroom"



    if type != 5:
        house = device.room.house
        ip = house.ip_address
        pintype = device.pin_type
        room = device.room

    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie ! nog oppassen want deze kan alleen smart devices aan '
    """
    #initialize()
    message = make_huge_string('change_status',room,device.ref_id,'status',value,str(pintype),'0')
    if not testing:
        Communicatie.SendInformation('%s:8080' % ip, message)


    # database updaten
    device.status = value
    device.save()
testing = True


####################################################
def read_prices():
    list = []
    with open('static/data/prijskwhperuur.csv') as datafile:
        datat = csv.reader(datafile, delimiter=';')
        for row in datat:
            list.append(row[1])
    return list


def read_zonneintensiteit():
    list = []
    with open('static/data/zonneintensiteitwattpervierkantemeter.csv') as datafile:
        datat = csv.reader(datafile, delimiter=';')
        for row in datat:
            list.append(row[1])
    return list


def read_windintensiteit():
    list = []
    with open('static/data/windinwijkmperseconde.csv') as datafile:
        datat = csv.reader(datafile, delimiter=';')
        for row in datat:
            list.append(row[1])
    return list

import os


def lees_basisconsumptie_slim_huis():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        datat = csv.reader(datafile, delimiter=';')
        rows = [row for row in datat]
        for row in rows[1:]:
            list.append(row[0])
    list = totaal_per_uur(list)
    return list


def lees_totaal_verbruik_dom_huis():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        datat = csv.reader(datafile, delimiter=';')
        rows = [row for row in datat]
        for row in rows[1:]:
            list.append(row[1])
    list = totaal_per_uur(list)
    return list


def lees_prijs_elektriciteit():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        datat = csv.reader(datafile, delimiter=';')
        rows = [row for row in datat]
        for row in rows[1:]:
            list.append(float(row[2]))
    list = gemiddelde_per_uur(list)
    return lis


def lees_zonneenergie():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        datat = csv.reader(datafile, delimiter=';')
        rows = [row for row in datat]
        for row in rows[1:]:
            list.append(row[3])
    list = totaal_per_uur(list)
    return list


def lees_buitentemperatuur():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        datat = csv.reader(datafile, delimiter=';')
        rows = [row for row in datat]
        for row in rows[1:]:
            list.append(row[4])
    list = gemiddelde_per_uur(list)
    return list


def totaal_per_uur(consumptie_per_kwartier):
    consumptie_per_uur = []
    while consumptie_per_kwartier != []:
        som = 0.
        for i in range(0,4):
            som += float(consumptie_per_kwartier[i])
        consumptie_per_uur.append(som)
        del consumptie_per_kwartier[0:4]
    return consumptie_per_uur
###########################################################

def gemiddelde_per_uur(consumptie_per_kwartier):
    consumptie_per_uur = []
    while consumptie_per_kwartier != []:
        som = 0
        for i in range(0,4):
            som += consumptie_per_kwartier[i]
        consumptie_per_uur.append(som/4)
        del consumptie_per_kwartier[0:4]
    return consumptie_per_uur
def getwind(time):
    list = read_windintensiteit()
    afgerondetijd = math.floor(time)  ### van 10:23 --> 10:00
    return list[time]
def getsolar(time):
    list = read_zonneintensiteit()
    afgerondetijd = math.floor(time)  ### van 10:23 --> 10:00
    return list[time]
def getprice(time):
    list = read_prices()
    afgerondetijd = math.floor(time)  ### van 10:23 --> 10:00
    return list[time]
def getcurplan(device,time):
    """
    haalt uit de database de huidige planning (in procent) in functie van de tijd

    """
def getcuruse(device):
    """
    geeft de huidige stand van het apparaat terug
    """



def make_huge_string(functie, room, unique, status, value, soort_pin, other_value,pin = 0):
    if soort_pin  ==0:
        soort_pin = None
    if pin ==0:
        pin = None
    if other_value ==0:
        other_value = None
    return 'function' + 'X' + str(functie) + 'Y' \
           + 'room' + 'X' + str(room) + 'Y'  \
            + 'uniqueid' + 'X' + str(unique) + 'Y'  \
            + 'paramtochange' + 'X' + str(status) +'Y'  \
            + 'status' + 'X' + str(value) + 'Y'  \
            + 'soort' + 'X' + str(soort_pin) + 'Y'  \
            + 'paramnewvalue' + 'X' + str(other_value) + 'Y'\
            + 'pinnumber' + 'X' + str(pin) +'Y'\



def initialize():
    data.append("START INITIALISEREN")
    data2.append("Dit file werkt")

    neigh = models.House.objects.all()

    ### itereren over alle apparaten ###
    for house in neigh:
        data.append("initialiseren - in house %s" % house.name)
        for room in house.room_set.all():
            data.append("initialiseren in room %s" % room.name)
            for smart_device in room.smart_devices_set.all():
                data.append("initialiseren van apparaat %s" % smart_device.ref_id)
                pintype = smart_device.pin_type
                message = make_huge_string('Initialise',str(room),str(smart_device.ref_id),'status','000',str(pintype),0,smart_device.pin_number)
                if not testing:
                    Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                smart_device.status = 000
                smart_device.save()
                change_status_2(smart_device.id, 000, 1)

            for fridge in room.fridges_set.all():
                data.append("initialiseren van apparaat %s" % fridge.ref_id)
                pintype = fridge.pin_type

                message = make_huge_string('Initialise', str(room), str(fridge.ref_id), 'status', '000', str(pintype),
                                           0, fridge.pin_number)
                if not testing:
                    Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                fridge.status = 000
                fridge.save()
                change_status_2(fridge.id, 000, 2)




            for battery in room.battery_set.all():
                data.append("initialiseren van apparaat %s" % battery.ref_id)

                pintype = battery.pin_type

                message = make_huge_string('Initialise', str(room), str(battery.ref_id), 'status', '000', str(pintype),
                                           0, battery.pin_number)
                if not testing:
                    Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                battery.status = 000
                battery.save()
                change_status_2(battery.id, 000, 3)






            for dumb_device in room.stupid_devices_set.all():
                data.append("initialiseren van apparaat %s" % dumb_device.ref_id)

                pintype = dumb_device.pin_type
                message = make_huge_string('Initialise', str(room), str(dumb_device.ref_id), 'status', '000', str(pintype),
                                           0, dumb_device.pin_number)
                if not testing:
                    Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                dumb_device.status = 000
                dumb_device.save()
                change_status_2(dumb_device.id, 000, 4)

        for heater in house.heating_set.all():
            data.append("initialiseren van apparaat %s" % heater.ref_id)

            pintype = heater.pin_type
            message = make_huge_string('Initialise', str('noroom'), str(heater.ref_id), 'status', '000', 'output',
                                       0, heater.pin_number)
            if not testing:
                Communicatie.SendInformation('%s:8080' % house.ip_address, message)
            heater.status = 000
            heater.save()
            change_status_2(heater.id, 000, 5)
    data.append("STOP INITIALISEREN\n")

def give_auxilary_file(request):
    with open('aux1.txt','w') as destinationfile:
        for row in data:
            destinationfile.write(row)
            destinationfile.write('\n')
    with open('aux2.txt','w') as destinationfile:
        for row in data2:
            destinationfile.write(row)
            destinationfile.write('\n')
    template = loader.get_template('neighbourhood/indexneighbourhood.html')
    return HttpResponse(template.render(request))




