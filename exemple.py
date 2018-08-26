#!/usr/bin/python
# -*- coding: utf-8 -*-
import librunner as mServer
# ARNY FAIT CA QUANT IL RECOIT LA COMMANDE 0x99
def F0X99(one):
    print "Je fais ça quand je reçois 0x99"
    return

def F0X98(one):
    print "Je fais ça quand je reçois 0x98"
    return

u = mServer.server('0.0.0.0',5656,'u')
u.attribAdd('0x99',F0X99)
u.attribAdd('0x98',F0X98)
u.DEBUG  = False
u.start() 