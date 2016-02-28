#!/usr/bin/env python
import socket
import sys
class device:
    def __init__(self):
        self.data=[]
    def ip(self,ip,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (ip, port)
        return self.sock
    def connect(self):
        print >>sys.stderr, 'connecting to %s port %s' % self.server_address
        try:
            self.sock.connect(self.server_address)
        except socket.error, e:
            print  >>sys.stderr, 'Connection refused or mobile not connected.'
            #raise e
            exit(0)
        return 
    def close(self):
        self.sock.close()
    def send(self,action):
        try:    
            print >>sys.stderr, 'sending "%s"' % action
            self.sock.sendall(action)
            while True:
                data = self.sock.recv(255)
                if data=="<201>":
                    break
                elif data=="<1>":
                    print  >>sys.stderr, 'Not Executed. Error reported.'
                    break
        except socket.error:
            print  >>sys.stderr, 'Connection refused or mobile not connected.'
            return "<1>"
        finally:
            print >>sys.stderr, 'Ending.'
            return "<0>"