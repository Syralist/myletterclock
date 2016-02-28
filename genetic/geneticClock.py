# -*- coding: utf-8 -*-
import re
import random
import math
import copy

TimePatternsDE = [
    "(.*)(ein)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(eins)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(eins)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(eins)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(eins)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(eins)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zwei)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zwei)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(zwei)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zwei)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(zwei)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zwei)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(zwei)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(zwei)(.*)",
    "(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(zwei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(zwei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(zwei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(zwei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(zwei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(zwei)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(drei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(drei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(drei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(drei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(drei)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(drei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(drei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(drei)(.*)",
    "(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(drei)(.*)",
    "(.*)(drei)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(drei)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(drei)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(drei)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(drei)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(drei)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(vier)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(vier)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(vier)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(vier)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(vier)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(vier)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(vier)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(vier)(.*)",
    "(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(vier)(.*)",
    "(.*)(vier)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(vier)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(vier)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(vier)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(vier)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(vier)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(fünf)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(fünf)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(fünf)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(fünf)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(fünf)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(fünf)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(fünf)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(fünf)(.*)",
    "(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(fünf)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(sechs)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(sechs)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(sechs)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(sechs)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(sechs)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(sechs)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(sechs)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(sechs)(.*)",
    "(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(sechs)(.*)",
    "(.*)(sechs)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(sechs)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(sechs)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(sechs)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(sechs)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(sechs)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(sieben)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(sieben)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(sieben)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(sieben)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(sieben)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(sieben)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(sieben)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(sieben)(.*)",
    "(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(sieben)(.*)",
    "(.*)(sieben)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(sieben)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(sieben)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(sieben)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(sieben)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(sieben)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(acht)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(acht)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(acht)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(acht)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(acht)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(acht)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(acht)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(acht)(.*)",
    "(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(acht)(.*)",
    "(.*)(acht)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(acht)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(acht)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(acht)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(acht)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(acht)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(neun)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(neun)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(neun)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(neun)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(neun)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(neun)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(neun)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(neun)(.*)",
    "(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(neun)(.*)",
    "(.*)(neun)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(neun)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(neun)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(neun)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(neun)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(neun)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zehn)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zehn)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(zehn)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zehn)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zehn)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(zehn)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(zehn)(.*)",
    "(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(elf)(.*)",
    "(.*)(elf)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(elf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(elf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(elf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(elf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(elf)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zwölf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zwölf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(zwölf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zwölf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(zwölf)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zwölf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(zwölf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(zwölf)(.*)",
    "(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(zwölf)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.*)",
    "(.*)(punkt)(.+)(zwölf)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(zwölf)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(zehn)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(zwölf)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    "(.*)(viertel)(.+)(nach)(.+)(zwölf)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(zwanzig)(.*)",
    "(.*)(zwanzig)(.+)(nach)(.+)(zwölf)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(eins)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(eins)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(dreissig)(.*)",
    "(.*)(halb)(.+)(eins)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    "(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(eins)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(vierzig)(.*)",
    "(.*)(zwanzig)(.+)(vor)(.+)(eins)(.*)",
    "(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(eins)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    "(.*)(drei)(.*)(viertel)(.+)(eins)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(fünfzig)(.*)",
    "(.*)(zehn)(.+)(vor)(.+)(eins)(.*)",
    "(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    "(.*)(fünf)(.+)(vor)(.+)(eins)(.*)"
    ]

Letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "ä",
    "ö",
    "ü"]

Words = [
    u"eins",
    u"zwei",
    u"drei",
    u"vier",
    u"fünf",
    u"sechs",
    u"sieben",
    u"acht",
    u"neun",
    u"zehn",
    u"elf",
    u"zwölf",
    u"viertel",
    u"zwanzig",
    u"halb",
    u"vor",
    u"nach",
    u"dreissig",
    u"vierzig",
    u"fünfzig",
    u"uhr",
    u"punkt"]

# print TimePatternsDE
TimePatternsRe = []
for p in TimePatternsDE:
    TimePatternsRe.append(re.compile(p))

# print TimePatternsRe

RectClock12x12StartPattern = list("XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX")

class GeneticClock():
    def __init__(self, StartPattern, Pop = 10):
        self.StartPattern = StartPattern
        self.BestPattern = StartPattern
        self.LastPattern = StartPattern
        self.ThisPattern = StartPattern
        self.PatternLength = len(self.StartPattern)
        self.PatternBreaks = self.StartPattern.count("|")
        self.PatternLetters = self.PatternLength - self.PatternBreaks
        self.BestFitness = 0
        self.Generation = 0
        self.Population = []
        for i in range(0, Pop):
            self.Population.append(list((StartPattern, 0)))
        self.LastPopulation = copy.deepcopy(self.Population)

    def Fitness(self, Pattern):
        numMatches = 0
        strPattern = "".join(Pattern)
        for r in TimePatternsRe:
            if r.match(strPattern):
                numMatches = numMatches + 1
        return numMatches

    def Mutate(self, rate = 0.10):
        num = int(math.floor(self.PatternLetters * rate))
        for i in range(0, num):
            rndLetter = Letters[random.randint(0,len(Letters)-1)]
            rndPosition = random.randint(0, self.PatternLength-1)
            if self.ThisPattern[rndPosition] == "|":
                rndPosition += 1
            self.ThisPattern[rndPosition] = rndLetter

    def InsertWord(self, Pattern):
        Pat = copy.deepcopy(Pattern)
        rndWord = random.choice(Words)
        rndWord = list(rndWord)
        rndPosition = random.randint(0, self.PatternLength-1-len(rndWord))
        offset = 0
        for l in rndWord:
            if Pat[rndPosition + offset] == "|":
                offset += 1
            Pat[rndPosition + offset] = l
            offset += 1
        return Pat

    def PrintPopulation(self):
        for P in self.Population:
            print "".join(P[0])
            print P[1]

    def run(self):
        while True:
            try:
                self.Generation += 1
                for i, P in enumerate(self.Population):
                    if self.LastPopulation[i][1] < self.BestFitness or self.BestFitness == 0:
                        P[0] = self.InsertWord(self.LastPopulation[i][0])
                    else:
                        P[0] = copy.deepcopy(self.LastPopulation[i][0])
                    P[1] = self.Fitness(P[0])
                    if P[1] > self.BestFitness:
                        self.BestFitness = P[1]

                self.LastPopulation = copy.deepcopy(self.Population)
                if self.Generation%100 == 0:
                    print "***" + str(self.Generation) + "***"
                    self.PrintPopulation()
            except KeyboardInterrupt:
                print "Interrupted"
                self.PrintPopulation()
                print self.Generation
                print self.BestFitness
                return
        
        

random.seed()
GC = GeneticClock(RectClock12x12StartPattern)
GC.run()
