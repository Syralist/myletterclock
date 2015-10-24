import pygame, led, sys, os, random, csv
from datetime import datetime 
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
gamestate = 1 #1=alive 0=dead

Cells = numpy.zeros((90, 20), dtype=numpy.int32)
Words = {}
Words['ES'] = ([1,1],[2,1])
Words["WAR"] = ([8,1],[9,1],[10,1])
Words["IST"] = ([12,1],[13,1],[14,1])
Words["WIRD"] = ([1,2],[2,2],[3,2],[4,2])
Words["GERADE"] = ([9,2],[10,2],[11,2],[12,2],[13,2],[14,2])
Words["GENAU"] = ([1,3],[2,3],[3,3],[4,3],[5,3])
Words["GLEICH"] = ([9,3],[10,3],[11,3],[12,3],[13,3],[14,3])
Words["FUENF1"] = ([1,4],[2,4],[3,4],[4,4])
Words["VIERTEL"] = ([8,4],[9,4],[10,4],[11,4],[12,4],[13,4],[14,4])
Words["ZEHN1"] = ([1,5],[2,5],[3,5],[4,5])
Words["ZWANZIG"] = ([8,5],[9,5],[10,5],[11,5],[12,5],[13,5],[14,5])
Words["HALB"] = ([1,6],[2,6],[3,6],[4,6])
Words["VOR1"] = ([7,6],[8,6],[9,6])
Words["NACH1"] = ([11,6],[12,6],[13,6],[14,6])
Words["EINS"] = ([1,7],[2,7],[3,7],[4,7])
Words["ZWEI"] = ([7,7],[8,7],[9,7],[10,7])
Words["DREI"] = ([11,7],[12,7],[13,7],[14,7])
Words["VIER"] = ([1,8],[2,8],[3,8],[4,8])
Words["FUENF2"] = ([11,8],[12,8],[13,8],[14,8])
Words["SECHS"] = ([1,9],[2,9],[3,9],[4,9],[5,9])
Words["SIEBEN"] = ([9,9],[10,9],[11,9],[12,9],[13,9],[14,9])
Words["ACHT"] = ([1,10],[2,10],[3,10],[4,10])
Words["NEUN"] = ([7,10],[8,10],[9,10],[10,10])
Words["ZEHN2"] = ([11,10],[12,10],[13,10],[14,10])
Words["ELF"] = ([1,11],[2,11],[3,11])
Words["ZWOELF"] = ([10,11],[11,11],[12,11],[13,11],[14,11])
Words["UHR"] = ([1,12],[2,12],[3,12])
Words["VOR2"] = ([8,12],[9,12],[10,12])
Words["NACH2"] = ([11,12],[12,12],[13,12],[14,12])
Words["MORGENS"] = ([1,13],[2,13],[3,13],[4,13],[5,13],[6,13],[7,13])
Words["MITTAG"] = ([8,13],[9,13],[10,13],[11,13],[12,13],[13,13],[14,13])
Words["NACHTS"] = ([1,14],[2,14],[3,14],[4,14],[5,14],[6,14])
Words["ABENDS"] = ([9,14],[10,14],[11,14],[12,14],[13,14],[14,14])
Months = {}
Months[1] = ([6,1])
Months[2] = ([6,2])
Months[3] = ([6,3])
Months[4] = ([6,4])
Months[5] = ([6,5])
Months[6] = ([6,6])
Months[7] = ([6,7])
Months[8] = ([6,8])
Months[9] = ([6,9])
Months[10] = ([6,10])
Months[11] = ([6,11])
Months[12] = ([6,12])
Day10 = {}
Day10[1] = ([3,1])
Day10[2] = ([4,1])
Day10[3] = ([5,1])
Day = {}
Day[0] = ([7,1])
Day[1] = ([7,2])
Day[2] = ([7,3])
Day[3] = ([7,4])
Day[4] = ([7,5])
Day[5] = ([7,6])
Day[6] = ([7,7])
Day[7] = ([7,8])
Day[8] = ([7,9])
Day[9] = ([7,10])
Texts = {}
Texts[0] = "Letterclock"
Texts[1] = "Hackerspace"
Texts[2] = "makehackmodify"

def setCell(x, y, c=IWHITE):
    global Cells
    try:
        Cells[x][y] = c
    except:
        pass

def light(word):
    for pixel in Words[word]:
        setCell(pixel[0],pixel[1])

def lightMonth(month):
    setCell(Months[month][0],Months[month][1],IRED)

def lightDay(day):
    if day >= 10:
        setCell(Day10[int(day/10)][0],Day10[int(day/10)][1],IGREEN)
    setCell(Day[day%10][0],Day[day%10][1],IGREEN)

def resetGame():
    global Cells
    for x in range(90):
        for y in range(20):
            Cells[x][y] = IBLACK

def main():
    global gamestate
    pygame.init()
    pygame.joystick.init()
    pygame.font.init()                                                                                                                                  
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
            second= datetime.now().second
            minute = datetime.now().minute
            minutemod5 = minute % 5
            hour = datetime.now().hour
            day = datetime.now().day
            month = datetime.now().month
            year = datetime.now().year
            
            resetGame()

            lightMonth(month)
            lightDay(day)
            
            light("ES")
            if minutemod5 == 1 or minutemod5 == 2:
                light("WAR")
                light("GERADE")
            if minutemod5 == 3 or minutemod5 == 4:
                light("WIRD")
                light("GLEICH")
            if minutemod5 == 0:
                light("IST")
                light("GENAU")
            if (minute >= 3 and minute <= 7) or (minute >= 23 and minute <= 27) or (minute >= 33 and minute <= 37) or (minute >= 53 and minute <= 57):
                light("FUENF1")
            if (minute >= 13 and minute <= 17) or (minute >= 43 and minute <= 47):
                light("VIERTEL")
            if (minute >= 8 and minute <= 12) or (minute >= 48 and minute <= 52):
                light("ZEHN1")
            if (minute >= 18 and minute <= 22) or (minute >= 38 and minute <= 42):
                light("ZWANZIG")
            if (minute >= 3 and minute <= 22) or (minute >= 33 and minute <= 37):
                light("NACH1")
            if (minute >= 23 and minute <= 27) or (minute >= 38 and minute <= 57):
                light("VOR1")
            if (minute >= 23 and minute <= 37):
                light("HALB")
            if ((hour ==  1 or hour == 13) and minute <= 22) or ((hour ==  0 or hour == 12) and minute >= 23):
                light("EINS")
            if ((hour ==  2 or hour == 14) and minute <= 22) or ((hour ==  1 or hour == 13) and minute >= 23):
                light("ZWEI")
            if ((hour ==  3 or hour == 15) and minute <= 22) or ((hour ==  2 or hour == 14) and minute >= 23):
                light("DREI")
            if ((hour ==  4 or hour == 16) and minute <= 22) or ((hour ==  3 or hour == 15) and minute >= 23):
                light("VIER")
            if ((hour ==  5 or hour == 17) and minute <= 22) or ((hour ==  4 or hour == 16) and minute >= 23):
                light("FUENF2")
            if ((hour ==  6 or hour == 18) and minute <= 22) or ((hour ==  5 or hour == 17) and minute >= 23):
                light("SECHS")
            if ((hour ==  7 or hour == 19) and minute <= 22) or ((hour ==  6 or hour == 18) and minute >= 23):
                light("SIEBEN")
            if ((hour ==  8 or hour == 20) and minute <= 22) or ((hour ==  7 or hour == 19) and minute >= 23):
                light("ACHT")
            if ((hour ==  9 or hour == 21) and minute <= 22) or ((hour ==  8 or hour == 20) and minute >= 23):
                light("NEUN")
            if ((hour ==  10 or hour == 22) and minute <= 22) or ((hour ==  9 or hour == 21) and minute >= 23):
                light("ZEHN2")
            if ((hour ==  11 or hour == 23) and minute <= 22) or ((hour ==  10 or hour == 22) and minute >= 23):
                light("ELF")
            if ((hour ==  12 or hour == 0) and minute <= 22) or ((hour ==  11 or hour == 23) and minute >= 23):
                light("ZWOELF")
            if minute >= 58 or minute <= 2:
                light("UHR")
            if (hour ==  22  and minute >= 23) or (hour >= 23 and hour <= 3) or (hour ==  4  and minute <= 22):
                light("NACHTS")
            if (hour ==  4  and minute >= 23) or (hour >= 5 and hour <= 8) or (hour ==  9  and minute <= 22):
                light("MORGENS")
            if (hour ==  9  and minute >= 23) or (hour >= 10 and hour <= 10) or (hour ==  11  and minute <= 22):
                light("VOR2")
                light("MITTAG")
            if (hour ==  11  and minute >= 23) or (hour ==  12  and minute <= 22):
                light("MITTAG")
            if (hour ==  12  and minute >= 23) or (hour >= 13 and hour <= 16) or (hour ==  17  and minute <= 22):
                light("NACH2")
                light("MITTAG")
            if (hour ==  17  and minute >= 23) or (hour >= 18 and hour <= 21) or (hour ==  22  and minute <= 22):
                light("ABENDS")
            # for key in Words:
            #     light(key)
            pygame.surfarray.blit_array(screen, Cells)
            font_text = pygame.font.SysFont(None, 16)
            text_text1 = Texts[minute%len(Texts)]
            write_text1 = font_text.render(text_text1, True, (0,255,0))
            screen.blit(write_text1, (17, 4))   
        else:
            pass

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
