import httplib
import time
#from neopixel import *
from random import randrange
#from Ledstrip import *
from NORXv3 import *

LED_COUNT = 59
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_INVERT = False

#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
#strip.begin()
#strip.setBrightness(150)
#Clearstrip(strip)

#URL VAN HET SMART HOUSE NOG INGEVEN!!
def SendInformation(URL,Message):
    global strip
    URL,Message = str(URL),encrypt_text(str(Message))[0]
#   if URL == '169.254.173.25:8080':
#        Ledstrip_CCU_To_HCU(strip, 10, 10)
    connectie = httplib.HTTPConnection(URL)
    UniqueURL = '/IncomingInformation/' + Message
    connectie.request('POST',UniqueURL)
    response = connectie.getresponse().status
#    if URL =='169.254.173.25:8080':
#        Ledstrip_HCU_To_CCU(strip, 10, 10)
    return str(response)


def GetInformation(URL,Message):
    global strip
    URL, Message = str(URL), encrypt_text(str(Message))[0]
    connectie = httplib.HTTPConnection(URL)
    UniqueURL = '/OutgoingInformation/'+ Message
    connectie.request('GET',UniqueURL)
    response = connectie.getresponse()
#    if URL =='169.254.173.25:8080':
#        Ledstrip_HCU_To_CCU(strip, 10, 10)
    return response.read()


def Test(URL):
    connectie = httplib.HTTPConnection(URL)
    UniqueURL = '/Test'
    connectie.request('GET', UniqueURL)
    response = connectie.getresponse()
    return response.read()


def SendLCD(URL,lijn1="leeg",lijn2="leeg"):
    URL,lijn1,lijn2 = str(URL),str(lijn1),str(lijn2)

    if ' ' in lijn1:
        temp_lijn1 = ''
        for i in range(0,len(lijn1)):
            if lijn1[i] != " ":
                temp_lijn1 += lijn1[i]
            else:
                temp_lijn1 += 'X'
        lijn1 = temp_lijn1

    if ' ' in lijn2:
        temp_lijn2 = ''
        for i in range(0,len(lijn2)):
            if lijn2[i] != " ":
                temp_lijn2 += lijn2[i]
            else:
                temp_lijn2 += 'X'
        lijn2 = temp_lijn2

    connectie = httplib.HTTPConnection(URL)
    UniqueURL = '/LCD/' + encrypt_text(lijn1)[0] + '/'+ encrypt_text(lijn2)[0]
    connectie.request('POST',UniqueURL)
    response = connectie.getresponse().status
    return str(response)

