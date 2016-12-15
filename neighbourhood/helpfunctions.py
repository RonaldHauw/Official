from models import *
from auxilary import *
import csv
import math
import Communicatie


#######################################################################
# CSV imports voor huidige omstandigheden
# geven vanuit het csv bestand een lijst terug met daarin ...
#######################################################################


def change_status_2(device_id, value, type):
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
    message = make_huge_string('change_status',device.room,device.ref_id,'status',value,str(pintype),'0')
    Communicatie.SendInformation('%s:8080' % ip, message) # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
    # de room waarnaar het moet gaan


    # database updaten
    device.status = value
    device.save()





def read_prices():
    list = []
    with open('static/data/prijskwhperuur.csv') as datafile:
        data = csv.reader(datafile, delimiter=';')
        for row in data:
            list.append(row[1])
    return list

def read_zonneintensiteit():
    list = []
    with open('static/data/zonneintensiteitwattpervierkantemeter.csv') as datafile:
        data = csv.reader(datafile, delimiter=';')
        for row in data:
            list.append(row[1])
    return list

def read_windintensiteit():
    list = []
    with open('static/data/windinwijkmperseconde.csv') as datafile:
        data = csv.reader(datafile, delimiter=';')
        for row in data:
            list.append(row[1])
    return list

import os
def lees_basisconsumptie_slim_huis():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        data = csv.reader(datafile, delimiter=';')
        rows = [row for row in data]
        for row in rows[1:]:
            list.append(row[0])
    list = totaal_per_uur(list)
    return list

def lees_totaal_verbruik_dom_huis():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        data = csv.reader(datafile, delimiter=';')
        rows = [row for row in data]
        for row in rows[1:]:
            list.append(row[1])
    list = totaal_per_uur(list)
    return list

def lees_prijs_elektriciteit():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        data = csv.reader(datafile, delimiter=';')
        rows = [row for row in data]
        for row in rows[1:]:
            list.append(float(row[2]))
    list = gemiddelde_per_uur(list)
    return list

def lees_zonneenergie():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        data = csv.reader(datafile, delimiter=';')
        rows = [row for row in data]
        for row in rows[1:]:
            list.append(row[3])
    list = totaal_per_uur(list)
    return list

def lees_buitentemperatuur():
    list = []
    #basisconsumptie per kwartier
    data_path = os.path.join(os.getcwd(), "neighbourhood","static", "data", "gegevens.csv")
    with open(data_path, "r") as datafile:
        data = csv.reader(datafile, delimiter=';')
        rows = [row for row in data]
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

def gemiddelde_per_uur(consumptie_per_kwartier):
    consumptie_per_uur = []
    while consumptie_per_kwartier != []:
        som = 0
        for i in range(0,4):
            som += consumptie_per_kwartier[i]
        consumptie_per_uur.append(som/4)
        del consumptie_per_kwartier[0:4]
    return consumptie_per_uur


def commit_change_old(appliance_id=None, value=None):
    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie
    """

    app = Smart_Devices.objects.get(id=appliance_id)
    room = app.room
    house = room.house
    pin = Smart_Devices.pin
    message = { 'function': commit_change,
                'room': room.shortcut,
                'unique_id': appliance_id,
                'param_to_change':'status',
                'new_value':value,
                'pin': pin}
    Communicatie.SendInformation('%s:8080' % house.ip, message) # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
    # de room waarnaar het moet gaan
def commit_change(appliance_id=None, value=None):
    """
    verandert de opgegeven parameter van een  apparaat in de gegeven value
    en stuurt dit door via informatie
    """

    app = Smart_Devices.objects.get(id=appliance_id)
    room = app.room
    house = room.house
    pin = Smart_Devices.pin
    message = { 'function': commit_change,
                'room': room.shortcut,
                'unique_id': appliance_id,
                'param_to_change':'status',
                'new_value':value,
                'pin': pin}
    Communicatie.SendInformation('%s:8080' % house.ip, message) # eerst de standaard url die naar het huis verwijst, in die huis bevat de message
    # de room waarnaar het moet gaan


##### 1 pagina, huisje aansturen met extra uitleg, tijdsklok,





def turnalloff():
    """
    zet de status van alle apparaten uit en daarmee ook het verbruik terug op nul. In zowel de database als in de huisjes
    !!!!!! initialisatie van alle apparaten !!!!!
    """
    neigh = House.objects.all()

    ### itereren over alle apparaten ###
    for house in neigh:
        for room in house.room_set.all():
            for smart_device in room.smart_devices_set.all():
                if smart_device.status != 000:
                    curid = smart_device.ref_id
                    commit_change(curid,000) ### verandering doorsturen naar huis
                    smart_device.status = 000 ### verandering doorsturen naar database


            for fridge in room.fridges_set.all():
                if fridge.status != 000:
                    curid = fridge.ref_id
                    commit_change(curid,000) ### verandering doorsturen naar huis
                    fridge.status = 000 ### verandering doorsturen naar database

            for battery in room.battery_set.all():
                if battery.status != 000:
                    curid = battery.ref_id
                    commit_change(curid,000) ### verandering doorsturen naar huis
                    battery.status = 000 ### verandering doorsturen naar database
            for heater in room.heating_set.all():
                if heater.status != 000:
                    curid = heater.ref_id
                    commit_change(curid,000) ### verandering doorsturen naar huis
                    heater.status = 000 ### verandering doorsturen naar database
            for dumb_device in room.stupid_devices_set.all():
                if dumb_device.status != 000:
                    curid = dumb_device.ref_id
                    commit_change(curid,000) ### verandering doorsturen naar huis
                    dumb_device.status = 000 ### verandering doorsturen naar database
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
def generate_code(house,room,type,id,status):
    pass
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

    neigh = House.objects.all()

    ### itereren over alle apparaten ###
    for house in neigh:
        for room in house.room_set.all():
            for smart_device in room.smart_devices_set.all():
                pintype = smart_device.pin_type
                message = make_huge_string('Initialise',str(room),str(smart_device.ref_id),'status','000',str(pintype),0,smart_device.pin_number)
                Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                smart_device.status = 000
                smart_device.save()
                change_status_2(smart_device.id, 000, 1)

            for fridge in room.fridges_set.all():
                pintype = fridge.pin_type

                message = make_huge_string('Initialise', str(room), str(fridge.ref_id), 'status', '000', str(pintype),
                                           0, fridge.pin_number)
                Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                fridge.status = 000
                fridge.save()
                change_status_2(fridge.id, 000, 2)




            for battery in room.battery_set.all():
                pintype = battery.pin_type

                message = make_huge_string('Initialise', str(room), str(battery.ref_id), 'status', '000', str(pintype),
                                           0, battery.pin_number)
                Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                battery.status = 000
                battery.save()
                change_status_2(battery.id, 000, 3)


            #for heater in room.Heating_set.all():
            #    message = make_huge_string('Initialise', str(room), str(smart_device.ref_id), 'status', '000', 'Output',
             #                              0, smart_device.pin_number)
             #   Communicatie.SendInformation('%s:8080' % house.ip_address, message)


            for dumb_device in room.stupid_devices_set.all():
                pintype = dumb_device.pin_type
                message = make_huge_string('Initialise', str(room), str(dumb_device.ref_id), 'status', '000', str(pintype),
                                           0, dumb_device.pin_number)
                Communicatie.SendInformation('%s:8080' % house.ip_address, message)
                dumb_device.status = 000
                dumb_device.save()
                change_status_2(dumb_device.id, 000, 4)


            # for heater in room.Heating_set.all():
            #     message = make_huge_string('Initialise', str(room), str(heater.ref_id), 'status', '000', 'Output',
            #                                0, dumb_device.pin_number)
            #     Communicatie.SendInformation('%s:8080' % house.ip_address, message)
            #     heater.status = 000
            #     heater.save()