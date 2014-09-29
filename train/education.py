#!/usr/bin/env python


import random
import numpy as np

def education():
    starttime = 1409001184244 + (1000*60*60*24)*random.choice(range(100))
    firstchartime = starttime + int((((random.random()*100000)+1) % 60000))
    endtime = firstchartime + random.choice(range(10, 80))*1000
    lastchartime = int(random.choice(np.linspace(firstchartime, endtime-1000, 100)[50:]))
    #print "fct: "+str(firstchartime-starttime)
    #print "lct: "+str(lastchartime-starttime)
    #print "end: "+str(endtime-starttime)
    print (endtime - starttime)

for x in xrange(100):
    education()
