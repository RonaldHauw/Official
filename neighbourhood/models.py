from __future__ import unicode_literals
from django.db import models

from django.db import models
import pandas as pd
from datetime import *
import helpfunctions

class Neighbourhood(models.Model):

    name = models.CharField(max_length=32)
    ref_id = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class House(models.Model):

    name = models.CharField(max_length=32)

    ip_address = models.CharField(max_length=32, default=0)
    ref_id = models.CharField(max_length=32, default=0)
    neighbourhood = models.ForeignKey(Neighbourhood)

    def __str__(self):
        return self.name

    def get_total_energy(self):

        ref_id = self.id
        print ref_id

        total_energy = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Energieverbruik': 0.})
        total_energy.set_index('Tijdstap', inplace=True)
        print total_energy

        if ref_id == 1:
            #dit is het slim huis. Nu wordt het totale verbruik berekend als de som van
            #verbruik per kamer(dit bevat alle smart devices) + basisconsumptie + verbruik frigo + verbruik verwarming +
            # verbruik batterij
            for room in self.room_set.all():
                print room
                tabel = room.get_total_energy()
                for i in range(len(tabel['Energieverbruik'])):
                    total_energy['Energieverbruik'] += tabel['Energieverbruik']
                    print total_energy


            app = Fridges.objects.filter(room__house=self)
            for a in app:
                total_energy += a.get_total_energy()

            app = Heating.objects.filter(house=self)
            for a in app:
                total_energy += a.get_total_energy()

            app = Battery.objects.filter(room__house=self)
            for a in app:
                total_energy += a.get_total_energy()

            basisconsumptie = helpfunctions.lees_basisconsumptie_slim_huis()
            print basisconsumptie
            for i in range(len(basisconsumptie)):
                total_energy['Energieverbruik'][i] += basisconsumptie[i]

        elif ref_id == 2:
            #dit is het 'domme' huis. Deze bevat enkel een basisverbruik
            totaalverbruik = helpfunctions.lees_totaal_verbruik_dom_huis()

            for i in range(len(totaalverbruik)):
                total_energy['Energieverbruik'][i] += totaalverbruik[i]

        return total_energy

    def get_total_price(self):

        total_price = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Price': 0.})
        total_price.set_index('Tijdstap', inplace=True)

        price_data = helpfunctions.lees_prijs_elektriciteit()
        print price_data

        total_energy = self.get_total_energy()

        for i, idx in enumerate(total_price.index):
            total_price.ix[idx,'Price'] = total_energy.ix[idx,'Energieverbruik']*price_data[i]/1000.

        return total_price

    def get_total_onlyprice(self):

        total_price = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Price': 0.})
        total_price.set_index('Tijdstap', inplace=True)

        price_data = helpfunctions.lees_prijs_elektriciteit()
        print price_data

        total_energy = self.get_total_energy()

        for i, idx in enumerate(total_price.index):
            total_price.ix[idx,'Price'] = price_data[i]

        return total_price



class Room(models.Model):

    #roomtypes = ((Kitchen,'Kitchen'),(Living_Room,'Living_Room'),(Hallway,'Hallway'),(Toilet,'Toilet'),(Laundry_Room,'Laundry_Room'),(Bedroom_1,'Bedroom_1'),(Bedroom_2,'Bedroom_2'),(Bathroom,'Bathroom'))

    house = models.ForeignKey(House)

    name = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=32, default=0)
    description = models.TextField()


    def __str__(self):
        return self.name + '-' + self.house.name

    def get_total_energy(self):

        total_energy = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Energieverbruik': 0.})
        total_energy.set_index('Tijdstap', inplace=True)

        for app in self.smart_devices_set.all():
            tabel = app.get_total_energy()
            total_energy['Energieverbruik'] += tabel['Energieverbruik']

        return total_energy

####################################################################################################
#nummer pin en soort van een pin
####################################################################################################
class Smart_Devices(models.Model):

    name = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    power = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)
    duration = models.CharField(max_length=100, default=0)
    deadline = models.CharField(max_length=100, default=0)
    begin_time = models.CharField(max_length=100, default=0)
    pin_number = models.CharField(max_length=100, default=0)
    pin_type = models.CharField(max_length=100, default=0)
    status_function = models.CharField(max_length=100, default=0)
    optimal_status = models.CharField(max_length=100, default=0)

    description = models.TextField()
    room = models.ForeignKey(Room)

    def __str__(self):
        return self.name + '-' + self.room.name

    def get_total_energy(self):
        """
        Berekent de totale energie van de apparaten per uur.
        :return:energy_usage: string met energieverbruik per uur
        """
        energy_usage = 0. #self.scheduled_consumption
        # ==> here there should be a link to the database model and the related time series

        total_energy = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Energieverbruik': energy_usage})
        total_energy.set_index('Tijdstap', inplace=True)

        return total_energy



class Fridges(models.Model):

    name = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    power = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)
    duration = models.CharField(max_length=100, default=0)
    begin_time = models.CharField(max_length=100, default=0)
    pin_number = models.CharField(max_length=100, default=0)
    pin_type = models.CharField(max_length=100, default=0)
    temperature = models.CharField(max_length=100, default=5)
    planned_status = models.CharField(max_length=100, default=0)
    optimal_status = models.CharField(max_length=100, default=0)


    description = models.TextField()
    room = models.ForeignKey(Room)

    def __str__(self):
        return self.name + '-' + self.room.name


    def get_total_energy(self):
        """
        Berekent de totale energie van de apparaten per uur.
        :return:energy_usage: string met energieverbruik per uur
        """
        energy_usage = 0. # TODO self.scheduled_consumption
        # ==> here there should be a link to the database model and the related time series

        total_energy = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Energieverbruik': energy_usage})
        total_energy.set_index('Tijdstap', inplace=True)

        return total_energy

####################################################################################################
####################################################################################################

class Heating(models.Model):

    name = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    power = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)
    duration = models.CharField(max_length=100, default=0)
    begin_time = models.CharField(max_length=100, default=0)
    pin_number = models.CharField(max_length=100, default=0)
    pin_type = models.CharField(max_length=100, default=0)
    planned_status = models.CharField(max_length=100, default=0)
    optimal_status = models.CharField(max_length=100, default=0)


    description = models.TextField()
    house = models.ForeignKey(House)

    def __str__(self):
        return self.name + '-' + self.room.name

    def get_total_energy(self):
        """
        Berekent de totale energie van de apparaten per uur.
        :return:energy_usage: string met energieverbruik per uur
        """
        energy_usage = 0. # TODO self.scheduled_consumption
        # ==> here there should be a link to the database model and the related time series

        total_energy = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Energieverbruik': energy_usage})
        total_energy.set_index('Tijdstap', inplace=True)

        return total_energy

####################################################################################################
####################################################################################################

class Battery(models.Model):

    name = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default=0)
    power = models.CharField(max_length=100, default=0)
    duration = models.CharField(max_length=100, default=0)
    begin_time = models.CharField(max_length=100, default=0)
    pin_number = models.CharField(max_length=100, default=0)
    pin_type = models.CharField(max_length=100, default=0)
    charge_status = models.CharField(max_length=100, default=40)
    optimal_status = models.CharField(max_length=100, default=0)
    charged_status = models.CharField(max_length=100, default=0)

    description = models.TextField()
    room = models.ForeignKey(Room)

    def __str__(self):
        return self.name + '-' + self.room.name

    def get_total_energy(self):
        """
        Berekent de totale energie van de apparaten per uur.
        :return:energy_usage: string met energieverbruik per uur
        """
        energy_usage = 0. # TODO self.scheduled_consumption
        # ==> here there should be a link to the database model and the related time series

        total_energy = pd.DataFrame(
            {'Tijdstap': pd.date_range(str(date.today()), periods=24, freq='60Min'),
             'Energieverbruik': energy_usage})
        total_energy.set_index('Tijdstap', inplace=True)

        return total_energy


class Stupid_Devices(models.Model):

    name = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    power = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)
    pin_number = models.CharField(max_length=100, default=0)
    pin_type = models.CharField(max_length=100, default=0)

    description = models.TextField()
    room = models.ForeignKey(Room)

    def __str__(self):
        return self.name + '-' + self.room.name


class Energy(models.Model):

    time = models.CharField(max_length=100, default=0)
    energy_price = models.CharField(max_length=100, default=0)
    used_energy = models.CharField(max_length=100, default=0)

    def __str__(self):
        return self.time + '-' + self.energy_price

# class Energy(models.Model):
#
#     time = models.CharField(max_length=100, default=0)
#     energy_price = models.CharField(max_length=100, default=0)
#     used_energy = models.CharField(max_length=100, default=0)
#
#     def __str__(self):
#         return self.time + '-' + self.energy_price




#all status


class Optimal_Status_Smart_Devices(models.Model):

    name = models.ForeignKey(Fridges)
    hour = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)

class Plan_Status_Fridges(models.Model):

    name = models.ForeignKey(Fridges)
    hour = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)

class Plan_Status_Heating(models.Model):

    name = models.ForeignKey(Heating)
    hour = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)


class Plan_Status_Battery(models.Model):

    name = models.ForeignKey(Battery)
    hour = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)

class Plan_Status_Stupid_devices(models.Model):

    name = models.ForeignKey(Stupid_Devices)
    hour = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)

#optimal status

class Optimal_Status_Fridges(models.Model):

    name = models.ForeignKey(Fridges)
    hour = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)

class Optimal_Status_Heating(models.Model):

    name = models.ForeignKey(Fridges)
    hour = models.CharField(max_length=100, default=0)
    status = models.CharField(max_length=100, default=0)








#class Plan_Status_Fridges(models.Model):
#
#    name = models.ForeignKey(Fridges)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
#class Plan_Status_Heating(models.Model):
#
#    name = models.ForeignKey(Heating)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
#
#class Plan_Status_Battery(models.Model):
#
#    name = models.ForeignKey(Battery)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
#class Plan_Status_Stupid_devices(models.Model):
#
#    name = models.ForeignKey(Stupid_Devices)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
##optimal status
#
#class Optimal_Status_Smart_Devices(models.Model):
#
#    name = models.ForeignKey(Fridges)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
#class Optimal_Status_Fridges(models.Model):
#
#    name = models.ForeignKey(Fridges)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
#class Optimal_Status_Heating(models.Model):
#
#    name = models.ForeignKey(Fridges)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
#class Optimal_Status_Battery(models.Model):
#
#    name = models.ForeignKey(Battery)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
#
#class Optimal_Status_Stupid_devices(models.Model):
#
#    name = models.ForeignKey(Stupid_Devices)
#    hour = models.CharField(max_length=100, default=0)
#    status = models.CharField(max_length=100, default=0)
#
#    def __str__(self):
#        return self.name + '-' + self.hour
