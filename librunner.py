#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import sys
import shlex, subprocess
import os
import re
import logging
import base64
from time import sleep
# les instructions de base 
fcts0 = ['RUN','I2C','LOAD','SAVE','POP','PUSH','LOG']
fcts1 = ['STO','RCL']
command = ['SERVER']
insts = command + fcts0 + fcts1
# les registres
registres = {   'A' : '' ,
                'B' : '' ,
                'C' : '' ,
                'D' : '' ,
                'E' : '' ,
                'BC': '',
                'DE': ''
            }
# SERVER STOP
#CLIENT
class device:
    def __init__(self):
        self.data=[]
        # definir ici vos besoin en variables spécifiques pour device()
        self.SERVER_STOP = base64.encodestring("SERVER STOP")
        self.SERVER_REGS = base64.encodestring("SERVER REGS")

    def token(self, texte):
        return base64.encodestring(texte)

    def ip(self,ip,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (ip, port)
        return self.sock

    def STO(self,registre,valeur):
        a = self.token("STO("+str(registre)+','+str(valeur)+")")
        r = self.send(a)
        return
    def RCL(self,registre):
        a = self.token("RCL("+str(registre)+")")
        r = self.send(a)
        return r

    def connect(self):
        print >>sys.stderr, 'connecting to %s port %s' % self.server_address
        try:
            self.sock.connect(self.server_address)
        except socket.error, e:
            print  >>sys.stderr, 'Connection refused or device not connected.'
            exit(0)
        return 
    def close(self):
        self.sock.close()
        return
    def send(self,action):
        action = self.token(action)
        try:    
            #print >>sys.stderr, 'sending "%s"' % action
            self.sock.sendall(action)
            #sleep(1)
            #while True:
            data = self.sock.recv(255)
            #print data
            if data == "<201>":
                print "Receive <201>"
                return "<0>"
            
            elif data == "<1>":
                print  >>sys.stderr, 'Not Executed. Error reported.'
                return "<1>"

            elif data=="<105>":
                print "Receive <105>"
                data = self.sock.recv(255)
                return data
            else:
                return data
        except socket.error:
            print  >>sys.stderr, 'Connection refused or device not connected.'
            return "<1>"

####SERVEUR
class server(object):
    """docstring for server"""

    def __init__(self, sip = "0.0.0.0" , sport = 5656):

        """ TEST          """
        self.ip = sip
        self.port = sport
        self.result = ""
        self.sock = []
        self.server_address = ()
        self.connection = []
        self.client_address = []
        
    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = (self.ip, self.port)
        self.sock.bind(self.server_address)
        self.sock.listen(1)

        while True:
            self.connection, self.client_address = self.sock.accept()
            try:
                while True:
                    data = self.connection.recv(255)
                    print >>sys.stderr, 'Receive ->', data
                    if data == "":
                        break
                    message = self.token(data)
                    # split fonction avec parametres entre parenthèse (la majorité des fonctions)
                    line = []   
                    for inst in insts:
                        t = message.find(inst,0,len(inst))
                        if t == 0 :
                            if inst in command :
                                line = message.split(" ")
                                break
                            elif inst in fcts0 :
                                l = message.split("'")
                                line = [inst]
                                line.append(l[1])
                                break
                            elif inst in fcts1 :
                                line = message.split("(")
                                line[1] = line[1].strip(")")
                                break
                        
                    print "INST:",line
                    if len(line) == 2 : 
                        if data:
                            self.result = self.interpretor(line)
                            if self.result == "<3>":
                                """ RIEN """
                            else:
                                self.connection.sendall(self.result)  
                            
                            self.connection.sendall("<201>")
                        else:
                            print >>sys.stderr, '<1>', self.client_address
                    else :
                        self.connection.sendall("<1>")
            except:
                #print "ERROR"
                raise
                self.connection.sendall("<1>")
            finally:
                #print "END"
                self.connection.close()

    def stop(self):
        print "Server Stop."
        self.connection.sendall("<201>")
        self.connection.close()
        exit()

    def RCL(self,registre):
        print "RCL"
        self.connection.sendall("<105>")
        self.connection.sendall(registres[registre])
        return "<3>"

    def form(self,phrase):
        sleep(0.5)
        if type(phrase) == 'str':
            return phrase
        if type(phrase) == 'list':
            return ','.join(phrase)
        return

    def interpretor(self,args):
        #args = shlex.split(action)
        # SERVER
        if args[0].upper() == "SERVER":
            if args[1].upper() == "REGS":
                print >>sys.stderr, registres
                return 

            if args[1].upper() == "STOP":
                self.stop()

        # RUN
        if args[0].upper() == "RUN":
            args0 = shlex.split(args[1])
            ecr = subprocess.check_output(args0).split()
            return '|'.join(ecr)
        # STO
        if args[0].upper() == "STO":
           args0 = args[1].split(",")
           aval = registres[args0[0]]
           registres[args0[0]] = args0[1]
           return aval
        # RCL
        if args[0].upper() == "RCL":
            print ">RCL"
            return "<0>"
    def token(self, texte):
        return base64.decodestring(texte)
        