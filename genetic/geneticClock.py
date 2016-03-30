# -*- coding: utf-8 -*-
import re
import random
import math
import copy
import os
from operator import itemgetter
from collections import deque

TimePatternsDEre = {
    1 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(eins)(.*)")
        ],
    2 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(eins)(.*)")
        ],
    3 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(eins)(.*)")
        ],
    4 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(eins)(.*)")
        ],
    5 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(eins)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zwei)(.*)")
        ],
    6 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zwei)(.*)")
        ],
    7 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(zwei)(.*)")
        ],
    8 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zwei)(.*)")
        ],
    9 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(zwei)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zwei)(.*)")
        ],
    10 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(zwei)(.*)")
        ],
    11 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(zwei)(.*)")
        ],
    12 : [
        re.compile(u"(.*)(ein)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(zwei)(.*)")
        ],
    13 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(zwei)(.*)")
        ],
    14 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(zwei)(.*)")
        ],
    15 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(zwei)(.*)")
        ],
    16 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(zwei)(.*)")
        ],
    17 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(zwei)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(drei)(.*)")
        ],
    18 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(drei)(.*)")
        ],
    19 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(drei)(.*)")
        ],
    20 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(drei)(.*)")
        ],
    21 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(drei)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(drei)(.*)")
        ],
    22 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(drei)(.*)")
        ],
    23 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(drei)(.*)")
        ],
    24 : [
        re.compile(u"(.*)(zwei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(drei)(.*)")
        ],
    25 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(drei)(.*)")
        ],
    26 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(drei)(.*)")
        ],
    27 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(drei)(.*)")
        ],
    28 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(drei)(.*)")
        ],
    29 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(drei)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(vier)(.*)")
        ],
    30 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(vier)(.*)")
        ],
    31 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(vier)(.*)")
        ],
    32 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(vier)(.*)")
        ],
    33 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(vier)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(vier)(.*)")
        ],
    34 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(vier)(.*)")
        ],
    35 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(vier)(.*)")
        ],
    36 : [
        re.compile(u"(.*)(drei)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(vier)(.*)")
        ],
    37 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(vier)(.*)")
        ],
    38 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(vier)(.*)")
        ],
    39 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(vier)(.*)")
        ],
    40 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(vier)(.*)")
        ],
    41 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(vier)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(fünf)(.*)")
        ],
    42 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(fünf)(.*)")
        ],
    43 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(fünf)(.*)")
        ],
    44 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(fünf)(.*)")
        ],
    45 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(fünf)(.*)")
        ],
    46 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(fünf)(.*)")
        ],
    47 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(fünf)(.*)")
        ],
    48 : [
        re.compile(u"(.*)(vier)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(fünf)(.*)")
        ],
    49 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(fünf)(.*)")
        ],
    50 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(fünf)(.*)")
        ],
    51 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(fünf)(.*)")
        ],
    52 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(fünf)(.*)")
        ],
    53 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(sechs)(.*)")
        ],
    54 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(sechs)(.*)")
        ],
    55 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(sechs)(.*)")
        ],
    56 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(sechs)(.*)")
        ],
    57 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(sechs)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(sechs)(.*)")
        ],
    58 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(sechs)(.*)")
        ],
    59 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(sechs)(.*)")
        ],
    60 : [
        re.compile(u"(.*)(fünf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(sechs)(.*)")
        ],
    61 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(sechs)(.*)")
        ],
    62 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(sechs)(.*)")
        ],
    63 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(sechs)(.*)")
        ],
    64 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(sechs)(.*)")
        ],
    65 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(sechs)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(sieben)(.*)")
        ],
    66 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(sieben)(.*)")
        ],
    67 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(sieben)(.*)")
        ],
    68 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(sieben)(.*)")
        ],
    69 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(sieben)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(sieben)(.*)")
        ],
    70 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(sieben)(.*)")
        ],
    71 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(sieben)(.*)")
        ],
    72 : [
        re.compile(u"(.*)(sechs)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(sieben)(.*)")
        ],
    73 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(sieben)(.*)")
        ],
    74 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(sieben)(.*)")
        ],
    75 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(sieben)(.*)")
        ],
    76 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(sieben)(.*)")
        ],
    77 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(sieben)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(acht)(.*)")
        ],
    78 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(acht)(.*)")
        ],
    79 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(acht)(.*)")
        ],
    80 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(acht)(.*)")
        ],
    81 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(acht)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(acht)(.*)")
        ],
    82 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(acht)(.*)")
        ],
    83 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(acht)(.*)")
        ],
    84 : [
        re.compile(u"(.*)(sieben)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(acht)(.*)")
        ],
    85 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(acht)(.*)")
        ],
    86 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(acht)(.*)")
        ],
    87 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(acht)(.*)")
        ],
    88 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(acht)(.*)")
        ],
    89 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(acht)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(neun)(.*)")
        ],
    90 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(neun)(.*)")
        ],
    91 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(neun)(.*)")
        ],
    92 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(neun)(.*)")
        ],
    93 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(neun)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(neun)(.*)")
        ],
    94 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(neun)(.*)")
        ],
    95 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(neun)(.*)")
        ],
    96 : [
        re.compile(u"(.*)(acht)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(neun)(.*)")
        ],
    97 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(neun)(.*)")
        ],
    98 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(neun)(.*)")
        ],
    99 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(neun)(.*)")
        ],
    100 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(neun)(.*)")
        ],
    101 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(neun)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zehn)(.*)")
        ],
    102 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zehn)(.*)")
        ],
    103 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(zehn)(.*)")
        ],
    104 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zehn)(.*)")
        ],
    105 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zehn)(.*)")
        ],
    106 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(zehn)(.*)")
        ],
    107 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(zehn)(.*)")
        ],
    108 : [
        re.compile(u"(.*)(neun)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(zehn)(.*)")
        ],
    109 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(zehn)(.*)")
        ],
    110 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(zehn)(.*)")
        ],
    111 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(zehn)(.*)")
        ],
    112 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(zehn)(.*)")
        ],
    113 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(elf)(.*)")
        ],
    114 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(elf)(.*)")
        ],
    115 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(elf)(.*)")
        ],
    116 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(elf)(.*)")
        ],
    117 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(elf)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(elf)(.*)")
        ],
    118 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(elf)(.*)")
        ],
    119 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(elf)(.*)")
        ],
    120 : [
        re.compile(u"(.*)(zehn)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(elf)(.*)")
        ],
    121 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(elf)(.*)")
        ],
    122 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(elf)(.*)")
        ],
    123 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(elf)(.*)")
        ],
    124 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(elf)(.*)")
        ],
    125 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(elf)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(zwölf)(.*)")
        ],
    126 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(zwölf)(.*)")
        ],
    127 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(zwölf)(.*)")
        ],
    128 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(zwölf)(.*)")
        ],
    129 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(zwölf)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(zwölf)(.*)")
        ],
    130 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(zwölf)(.*)")
        ],
    131 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(zwölf)(.*)")
        ],
    132 : [
        re.compile(u"(.*)(elf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(zwölf)(.*)")
        ],
    133 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.*)"),
        re.compile(u"(.*)(punkt)(.+)(zwölf)(.*)")
        ],
    134 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(zwölf)(.*)")
        ],
    135 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(zehn)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(zwölf)(.*)")
        ],
    136 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(zehn)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(nach)(.+)(zwölf)(.*)")
        ],
    137 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(zwanzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(nach)(.+)(zwölf)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(halb)(.+)(eins)(.*)")
        ],
    138 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(zwanzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(halb)(.+)(eins)(.*)")
        ],
    139 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(dreissig)(.*)"),
        re.compile(u"(.*)(halb)(.+)(eins)(.*)")
        ],
    140 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(dreissig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(nach)(.+)(halb)(.+)(eins)(.*)")
        ],
    141 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(vierzig)(.*)"),
        re.compile(u"(.*)(zwanzig)(.+)(vor)(.+)(eins)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(nach)(.+)(halb)(.+)(eins)(.*)")
        ],
    142 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(vierzig)(.*)"),
        re.compile(u"(.*)(viertel)(.+)(vor)(.+)(eins)(.*)")
        ],
    143 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(fünfzig)(.*)"),
        re.compile(u"(.*)(zehn)(.+)(vor)(.+)(eins)(.*)")
        ],
    144 : [
        re.compile(u"(.*)(zwölf)(.+)(uhr)(.+)(fünf)(.*)(und)(.*)(fünfzig)(.*)"),
        re.compile(u"(.*)(fünf)(.+)(vor)(.+)(eins)(.*)")
        ]
    }

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
    u"(.*)(viertel)(.+)(vor)(.+)(zwei)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(drei)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(vier)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(fünf)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(sechs)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(sieben)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(acht)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(neun)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(zehn)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(elf)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(zwölf)(.*)",
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
    u"(.*)(viertel)(.+)(vor)(.+)(eins)(.*)",
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
    u"und",
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
        self.LastPattern = StartPattern
        self.ThisPattern = StartPattern
        self.PatternLength = len(self.StartPattern)
        self.PatternBreaks = self.StartPattern.count("|")
        self.PatternLetters = self.PatternLength - self.PatternBreaks
        self.BestFitness = 0
        self.BestFitness2 = 0
        self.Generation = 0
        self.Population = []
        for i in range(0, Pop):
            self.Population.append(list((StartPattern, 0)))
        self.LastPopulation = copy.deepcopy(self.Population)
        self.BestPatterns = deque([],10)

    def Fitness(self, Pattern):
        numMatches = 0
        strPattern = "".join(Pattern)
        for r in TimePatternsRe:
            if r.match(strPattern):
                numMatches = numMatches + 1
        return numMatches

    def Fitness2(self, Pattern):
        numMatches = 0
        numTimes = 0
        timeMatched = False
        strPattern = "".join(Pattern)
        for i, r in TimePatternsDEre.iteritems():
            timeMatched = False
            for t in r:
                if t.match(strPattern):
                    numMatches = numMatches + 1
                    if not timeMatched:
                        timeMatched = True
                        numTimes = numTimes + 1
        return numMatches, numTimes

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
        rndPosition = random.randint(0, self.PatternLength-len(rndWord))
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

    def PrintBestPattern(self):
        for P in self.BestPatterns:
            num, times = self.Fitness2(P[0])
            print "".join(P[0])
            # print P[1], float(P[1])/float(len(TimePatternsDEre))
            print times, float(times)/float(len(TimePatternsDEre))
            print num, float(num)/float(len(TimePatternsRe))

    def run(self):
        # while self.Generation < 10:
        while True:
            try:
                self.Generation += 1
                for i, P in enumerate(self.Population):
                    if self.LastPopulation[i][1] < self.BestFitness or self.BestFitness == 0 or self.Generation%10 == 0:
                        P[0] = self.InsertWord(self.LastPopulation[i][0])
                    else:
                        P[0] = copy.deepcopy(self.LastPopulation[i][0])
                    dummy, P[1] = self.Fitness2(P[0])
                    if P[1] > self.BestFitness:
                        self.BestFitness = P[1]
                        self.BestPatterns.appendleft(copy.deepcopy(P))

                self.Population = sorted(self.Population, key=itemgetter(1), reverse=True)
                self.CombinePattern(self.Population[0][0],self.Population[1][0])
                # self.Population[-2][1] = self.Fitness(self.Population[-2][0])
                dummy, self.Population[-2][1] = self.Fitness2(self.Population[-2][0])
                if self.Population[-2][1] > self.BestFitness:
                    self.BestFitness = self.Population[-2][1]
                dummy, self.Population[-1][1] = self.Fitness2(self.Population[-1][0])
                if self.Population[-1][1] > self.BestFitness:
                    self.BestFitness = self.Population[-1][1]
                self.Population = sorted(self.Population, key=itemgetter(1), reverse=True)

                self.LastPopulation = copy.deepcopy(self.Population)
                if self.Generation%100 == 0:
                # if True:
                    print "***" + str(self.Generation) + "***"
                    # self.PrintPopulation()
                    self.PrintBestPattern()
                    print self.BestFitness
            except KeyboardInterrupt:
                print "Interrupted"
                print "After", self.Generation, "Generations, these are the Best Patterns:"
                self.PrintBestPattern()
                # self.PrintPopulation()
                # print self.BestFitness
                return
        
        

random.seed()
GC = GeneticClock(RectClock12x12StartPattern)
GC.run()




