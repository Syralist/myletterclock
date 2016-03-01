# -*- coding: utf-8 -*-
import re
import random
import math
import copy
from operator import itemgetter

TimePatternsDE = [
    u"(.*)(ein)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(eins)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(eins)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(eins)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(eins)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(eins)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zwei)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zwei)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(zwei)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zwei)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(zwei)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zwei)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(zwei)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(zwei)(.*)",
    u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(zwei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(zwei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(zwei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(zwei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(zwei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(zwei)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(drei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(drei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(drei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(drei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(drei)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(drei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(drei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(drei)(.*)",
    u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(drei)(.*)",
    u"(.*)(drei)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(drei)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(drei)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(drei)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(drei)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(drei)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(vier)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(vier)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(vier)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(vier)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(vier)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(vier)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(vier)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(vier)(.*)",
    u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(vier)(.*)",
    u"(.*)(vier)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(vier)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(vier)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(vier)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(vier)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(vier)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(fünf)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(fünf)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(fünf)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(fünf)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(fünf)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(fünf)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(fünf)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(fünf)(.*)",
    u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(fünf)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(sechs)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(sechs)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(sechs)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(sechs)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(sechs)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(sechs)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(sechs)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(sechs)(.*)",
    u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(sechs)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(sechs)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(sechs)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(sechs)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(sechs)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(sechs)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(sieben)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(sieben)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(sieben)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(sieben)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(sieben)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(sieben)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(sieben)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(sieben)(.*)",
    u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(sieben)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(sieben)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(sieben)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(sieben)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(sieben)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(sieben)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(acht)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(acht)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(acht)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(acht)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(acht)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(acht)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(acht)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(acht)(.*)",
    u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(acht)(.*)",
    u"(.*)(acht)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(acht)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(acht)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(acht)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(acht)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(acht)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(neun)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(neun)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(neun)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(neun)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(neun)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(neun)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(neun)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(neun)(.*)",
    u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(neun)(.*)",
    u"(.*)(neun)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(neun)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(neun)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(neun)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(neun)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(neun)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zehn)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zehn)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(zehn)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zehn)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zehn)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(zehn)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(zehn)(.*)",
    u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(elf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(elf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(elf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(elf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(elf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(elf)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zwölf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zwölf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(zwölf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zwölf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(zwölf)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zwölf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(zwölf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(zwölf)(.*)",
    u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(zwölf)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.*)",
    u"(.*)(punkt)(.+)(zwölf)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(zwölf)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(zehn)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(zwölf)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)",
    u"(.*)(viertel)(.+)(nach)(.+)(zwölf)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(zwanzig)(.*)",
    u"(.*)(zwanzig)(.+)(nach)(.+)(zwölf)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(eins)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(eins)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(dreissig)(.*)",
    u"(.*)(halb)(.+)(eins)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)",
    u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(eins)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(vierzig)(.*)",
    u"(.*)(zwanzig)(.+)(vor)(.+)(eins)(.*)",
    u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(eins)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)",
    u"(.*)(drei)(.*)(viertel)(.+)(eins)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(fünfzig)(.*)",
    u"(.*)(zehn)(.+)(vor)(.+)(eins)(.*)",
    u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)",
    u"(.*)(fünf)(.+)(vor)(.+)(eins)(.*)"
    ]

Letters = [
    u"a",
    u"b",
    u"c",
    u"d",
    u"e",
    u"f",
    u"g",
    u"h",
    u"i",
    u"j",
    u"k",
    u"l",
    u"m",
    u"n",
    u"o",
    u"p",
    u"q",
    u"r",
    u"s",
    u"t",
    u"u",
    u"v",
    u"w",
    u"x",
    u"y",
    u"z",
    u"ä",
    u"ö",
    u"ü"]

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

RectClock12x12StartPattern = list(u"XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX|XXXXXXXXXXXX")

class GeneticClock():
    def __init__(self, StartPattern, Pop = 15):
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

    def CombinePattern(self, PatternA, PatternB):
        PatA1 = PatternA[:int(math.floor(self.PatternLength/2))]
        PatA2 = PatternA[int(math.floor(self.PatternLength/2)):]
        PatB1 = PatternB[:int(math.floor(self.PatternLength/2))]
        PatB2 = PatternB[int(math.floor(self.PatternLength/2)):]
        self.Population[-1][0] = copy.deepcopy(PatA1+PatB2)
        self.Population[-2][0] = copy.deepcopy(PatB1+PatA2)


    def PrintPopulation(self):
        for P in self.Population:
            print "".join(P[0])
            print P[1]

    def run(self):
        # while self.Generation < 10:
        while True:
            try:
                self.Generation += 1
                for i, P in enumerate(self.Population):
                    if self.LastPopulation[i][1] < self.BestFitness or self.BestFitness == 0 or self.Generation%2 == 0:
                        P[0] = self.InsertWord(self.LastPopulation[i][0])
                    else:
                        P[0] = copy.deepcopy(self.LastPopulation[i][0])
                    P[1] = self.Fitness(P[0])
                    if P[1] > self.BestFitness:
                        self.BestFitness = P[1]

                self.Population = sorted(self.Population, key=itemgetter(1), reverse=True)
                self.CombinePattern(self.Population[0][0],self.Population[1][0])
                self.Population[-2][1] = self.Fitness(self.Population[-2][0])
                if self.Population[-2][1] > self.BestFitness:
                    self.BestFitness = self.Population[-2][1]
                self.Population[-1][1] = self.Fitness(self.Population[-1][0])
                if self.Population[-1][1] > self.BestFitness:
                    self.BestFitness = self.Population[-1][1]
                self.Population = sorted(self.Population, key=itemgetter(1), reverse=True)

                self.LastPopulation = copy.deepcopy(self.Population)
                if self.Generation%100 == 0:
                # if True:
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
