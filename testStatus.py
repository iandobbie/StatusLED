#!/usr/bin/env python

# Test DeepSIM status lights.

import opc, time, copy
import math
import numpy as N

PI = 3.14159
outerLEDs=24
innerLEDs=12
totalLEDs = (innerLEDs+outerLEDs)


#Setup stuff.

power = 128



class StatusLED():
    def __init__(self):
        self.client = opc.Client('localhost:7890')
        #make an intensity array for the whole fadecandy addressable pixels.
        self.intensity = [(0,0,0)] * 512 
        #inital ppower level is 100 (out of 255)
        self.power = 100
        self.outerLEDs=outerLEDs
        self.innerLEDs=innerLEDs
        self.totalLEDs=(outerLEDs+innerLEDs)
        self.start=(512-64)
        self.progress=0
        self.savedProgress=(0,0,0)
        
    #Function to call on an image snap
    def onSnap(self,t=0.1):
        pulseIntensity=copy.copy(self.intensity)
        for i in range(self.outerLEDs):
            pulseIntensity[self.start+i]=(self.power,self.power,self.power)
        self.pulseLEDs(pulseIntensity,t)


    def onError(self,t=1.0):
        pulseIntensity=copy.copy(self.intensity)
        for i in range(outerLEDs):
            pulseIntensity[self.start+i]=(self.power,0,0)
        for i in range(5):
            self.pulseLEDs(pulseIntensity,t)
            time.sleep(1.0)

    def setWhite(self):
        for i in range(self.totalLEDs):
            self.intensity[self.start+i]=(self.power,self.power,self.power)
        self.setLEDs(None)

    def setOff(self):
        for i in range(self.totalLEDs):
            self.intensity[self.start+i]=(0,0,0)
        self.setLEDs(None)
    

    def pulseLEDs(self,pulseIntensity,t=0.1):
        self.setLEDs(None)
        self.setLEDs(pulseIntensity)
        time.sleep(float(t))
        self.setLEDs(pulseIntensity)
        self.setLEDs(None)
        
    def setLEDs(self,intensity):
        if intensity is None:
            self.client.put_pixels(self.intensity)
            self.client.put_pixels(self.intensity)
        else:
            self.client.put_pixels(intensity)
            self.client.put_pixels(intensity)


    def setInner(self,col=(1,1,1)):
        for i in range(self.innerLEDs):
            self.intensity[self.start+self.outerLEDs+i]=(col)
        self.setLEDs(None)

    

    def setOuter(self,col):
        for i in range(self.outerLEDs):
            self.intensity[self.start+i]=(col)
        self.setLEDs(None)

    def incProgress(self,col=(0,100,0)):
        self.intensity[self.start+self.progress]=self.savedProgress
        self.progress=self.progress+1
        if self.progress>(self.outerLEDs-1):
            self.progress=0
        self.savedProgress=copy.copy(self.intensity[self.start+self.progress])
        self.intensity[self.start+self.progress]=col
        self.setLEDs(None)

    def stopProgress(self):
        self.intensity[self.start+self.progress]=self.savedProgress
        self.setLEDs(None)
