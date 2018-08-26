#!/usr/bin/python
# -*- coding: utf-8 -*-
import librunner as mServer
# ARNY FAIT CA QUANT IL RECOIT LA COMMANDE 0x99
def F0X99(one):
    print "JE fais ça quand je reçois 0x99"
    aa = 9 
    print aa*6
    return 
def F0x98():
    print "JE fais ça quand je reçois 0x98"
arnyCom  = mServer.server('0.0.0.0',5656,'arnyCom')
arnyCom.attribAdd('0x99',F0X99)
arnyCom.DEBUG  = False
#START ARNY'S COMMUNICATION CAPACITIES
arnyCom.start() 