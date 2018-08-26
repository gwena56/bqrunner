#!/usr/bin/python
# -*- coding: utf-8 -*-
import librunner as mServer
vitesse = 50
duree = 100   
def F0X99(fake):
    print "Je fais ça quand je reçois 0x99"
    return 
def avant(fake):
    print "Je fais ça quand je reçois 0x98"
    print vitesse, duree
    return
arnyCom = mServer.server('0.0.0.0',5656,'arnyCom')
arnyCom.DEBUG = False
arnyCom.attribAdd('0x99',F0X99)
arnyCom.attribAdd('0x98',oled)
arnyCom.start()