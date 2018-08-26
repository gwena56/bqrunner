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
from types import MethodType
# les instructions de base 

# les registres
# SERVER STOP
#CLIENT
class device:
    def __init__(self):
        self.data=[]
        self.ENCODE=False
        # definir ici vos besoin en variables spécifiques pour device()
        self.SERVER_STOP = base64.encodestring("SERVER STOP")
        self.SERVER_REGS = base64.encodestring("SERVER REGS")

    def token(self, texte):
        if self.ENCODE == False:
            return texte
        else:
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
    class quoifaire(object):
        """docstring for ClassName"""
        #def __init__(self):
        #    """ NONE """
        pass
            
    def __init__(self, sip = "0.0.0.0" , sport = 5656, name = 'no-name'):
        """ TEST          """
        self.ip = sip
        self.port = sport
        self.name = name
        self.result = ""
        self.sock = []
        self.server_address = ()
        self.connection = []
        self.client_address = []
        self.ENCODE = False
        self.DEBUG = True
        self.fcts = ['EXEC','RUN']
        self.userdefs = {}
        self.command = ['SERVER']
        self.insts = self.command + self.fcts
        self.registres = {   'A' : '' ,
                'B' : '' ,
                'C' : '' ,
                'D' : '' ,
                'E' : '' ,
                'F' : '' ,
                'G' : ''
            }
 
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
                    if self.DEBUG == 1:
                        print >>sys.stderr, self.name + ' Receive ', data
                    if data == "":
                        break
                    message = self.token(data)
                    # split fonction avec parametres entre parenthèse (la majorité des fonctions)
                    line = []   
                    for inst in self.insts:
                        t = message.find(inst,0,len(inst))
                        if t == 0 :
                            if  inst in self.command :
                                line = message.split(" ")
                                break
                            elif inst in self.fcts :
                                l = message.split("'")
                                line = [inst]
                                line.append(l[1])
                                break
                        
                    if self.DEBUG == 1:
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
        if self.DEBUG == 1:
            print "Server Stop."
        self.connection.sendall("<201>")
        self.connection.close()
        exit()

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
                print >>sys.stderr, self.registres
                return '<3>'
            if args[1].upper() == "ALIVE":
                print >>sys.stderr, self.name + " is alive @"+self.ip+":"+str(self.port)
                return '<3>'
            if args[1].upper() == "STOP":
                self.stop()
        # EXEC
        if args[0].upper() == "EXEC":
            args0 = shlex.split(args[1])
            ecr = subprocess.check_output(args0).split()
            print >>sys.stderr, ecr
            return '|'.join(ecr)
        # dict interpretor
        # RUN
        if args[0].upper() == "RUN":
            print args[1]
            if self.userdefs.has_key(args[1]):
                ff = self.quoifaire()
                self.quoifaire.fonct = self.userdefs[args[1]]
                ff.fonct()
                return '<3>'
            else:
                return '<1>'
    def token(self, texte):
        if self.ENCODE == False:
            return texte
        else:
            return base64.encodestring(texte)
    def attribAdd(self,fct,extFct):
        if self.DEBUG == 1:
            print 'New server atribution created as ',fct,' memory instance ',extFct
        self.userdefs[fct] = extFct
        return '<3>'