import time
from neopixel import *
from random import randrange





def colorWipe(strip, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColorRGB(i, 255, 0, 0)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def Ledstrip_CCU_To_HCU(strip, length=6, wait_ms=50):

    for i in range((strip.numPixels())):
        strip.setPixelColorRGB(i,randrange(0,255,1),randrange(0,255,1),randrange(0,255,1))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        if i >= length :
            strip.setPixelColorRGB(i - length, 0, 0, 0)
            strip.show()
            time.sleep(wait_ms/1000.0)
    for j in range(strip.numPixels()-length,strip.numPixels()):
        strip.setPixelColorRGB(j,0,0,0)
        strip.show()
        time.sleep(wait_ms/1000.0)


def Ledstrip_HCU_To_CCU(strip, lenght=6, wait_ms=50):
    for i in range((strip.numPixels())-1,-1,-1):
        strip.setPixelColorRGB(i,randrange(0,255),randrange(0,255) ,randrange(0,255))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        if strip.numPixels()-lenght >= i :
            strip.setPixelColorRGB(i+lenght,0,0,0)
            strip.show()
            time.sleep(wait_ms/1000.0)

    for j in range(lenght,-1,-1):
        strip.setPixelColorRGB(j,0,0,0)
        strip.show()
        time.sleep(wait_ms/1000.0)


def Clearstrip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColorRGB(i,0,0,0)
        strip.show()




