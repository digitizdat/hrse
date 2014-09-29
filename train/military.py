#!/usr/bin/env python


import random
import numpy as np

def military():
    starttime = 1409001184244 + (1000*60*60*24)*random.choice(range(100))
    firstchartime = starttime + int((((random.random()*100000)+1) % 60000))
    endtime = firstchartime + random.choice(range(10, 60))*1000
    choices = np.linspace(firstchartime, endtime-1000, 100)[50:]
    lastchartime = int(random.choice(choices))
    #print "fct: "+str(firstchartime-starttime)
    #print "lct: "+str(lastchartime-starttime)
    #print "end: "+str(endtime-starttime)
    if (endtime - lastchartime) < 3000:
        print "Yes"
    else:
        print "No"


for x in xrange(100):
    military()
