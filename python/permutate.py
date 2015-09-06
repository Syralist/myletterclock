# -*- coding: utf-8 -*-
import itertools

Breite = 14
Stunden = ["Eins", "Zwei", "Drei", "Vier", "Fünf", "Sechs", "Sieben", "Acht", "Neun", "Zehn", "Elf", "Zwölf"]

Combis2 = list(itertools.combinations(Stunden, 2))
Combis3 = list(itertools.combinations(Stunden, 3))
Combis4 = list(itertools.combinations(Stunden, 4))

for c in Combis2:
    w = ''.join(c)
    if len(w) <= Breite - 1:
        print w
for c in Combis3:
    w = ''.join(c)
    if len(w) <= Breite - 2:
        print w
for c in Combis4:
    w = ''.join(c)
    if len(w) <= Breite - 3:
        print w
