#!/usr/bin/python
# -*- coding: utf-8 -*-
import librunner as mServer
serveur  = cServer.server('0.0.0.0',5650,'MonServeur')
serveur.DEBUG  = True
serveur.start()