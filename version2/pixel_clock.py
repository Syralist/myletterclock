import pygame, led, sys, os, random, csv
import numpy
from pygame.locals import *
from led.PixelEventHandler import *
# from bmpfont import bmpfont

""" A Letterclock for Pixel Display
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
IWHITE = 16777215
IRED = 16711680
IGREEN = 65280
IBLUE = 255
IBLACK = 0

# wing1font = bmpfont.BmpFont("bmpfont/wing1-5x5px-white.idx")

# detect if a serial/USB port is given as argument
hasSerialPortParameter = ( sys.argv.__len__() > 1 )

# use 90 x 20 matrix when no usb port for real display provided
fallbackSize = ( 90, 20 )

if hasSerialPortParameter:
    serialport = sys.argv[ 1 ]
    print "INITIALIZING WITH USB-PORT: "+serialport
    ledDisplay = led.dsclient.DisplayServerClientDisplay(serialport, 8123)
else:
    print "INITIALIZING WITH SIMULATOR ONLY."
    ledDisplay = led.dsclient.DisplayServerClientDisplay("localhost", 8123)

# use same size for sim and real LED panel
size = ledDisplay.size()
simDisplay = led.sim.SimDisplay(size)
screen = pygame.Surface(size)
gamestate = 1 #1=alive; 0=dead

Cells = numpy.zeros((90, 20), dtype=numpy.int32)
Words = {}
Words['ES'] = ([1,1],[2,1])
Words["WAR"] = ()
Words["IST"] = ()
Words["WIRD"] = ()
Words["GLEICH"] = ()
Words["GENAU"] = ()
Words["GERADE"] = ()
Words["FÜNF1"] = ()
Words["VIERTEL"] = ()
Words["ZEHN1"] = ()
Words["ZWANZIG"] = ()
Words["HALB"] = ()
Words["VOR1"] = ()
Words["NACH1"] = ()
Words["EINS"] = ()
Words["ZWEI"] = ()
Words["DREI"] = ()
Words["VIER"] = ()
Words["FÜNF2"] = ()
Words["SECHS"] = ()
Words["SIEBEN"] = ()
Words["ACHT"] = ()
Words["NEUN"] = ()
Words["ZEHN2"] = ()
Words["ELF"] = ()
Words["ZWÖLF"] = ()
Words["UHR"] = ()
Words["VOR2"] = ()
Words["NACH2"] = ()
Words["MITTAG"] = ()
Words["NACHTS"] = ()
Words["MORGENS"] = ()
Words["ABENDS"] = ()


def setCell(x, y):
    global Cells
    try:
        Cells[x][y] = IWHITE
    except:
        pass

def light(word):
    for pixel in Words[word]:
        setCell(pixel[0],pixel[1])

def resetGame():
    global Cells
    for x in range(90):
        for y in range(20):
            Cells[x][y] = IBLACK

def main():
    global gamestate
    pygame.init()
    pygame.joystick.init()
    # Initialize first joystick
    if pygame.joystick.get_count() > 0:
        stick = pygame.joystick.Joystick(0)
        stick.init()
    clock = pygame.time.Clock()
    
    resetGame()

    while True:
        for pgevent in pygame.event.get():
            event = process_event(pgevent)
            # if event.button == EXIT:
            #     pygame.quit()
            #     sys.exit()

            if event.type == PUSH:
                if event.button == UP:
                    pass
                elif event.button == DOWN:
                    pass
                elif event.button == LEFT:
                    pass
                elif event.button == RIGHT:
                    pass
                elif event.button == B1:
                    pass
                elif event.button == P1:
                    pygame.quit()
                    sys.exit()

        if gamestate == 1:
            light('ES')
            pygame.surfarray.blit_array(screen, Cells)
        else:
            pass

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
