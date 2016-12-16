#!/usr/bin/env python

# Test DeepSIM status lights.

import opc, time, copy
import math
import numpy as N

PI = 3.14159
ringStart=(512-64)
outerLEDs=24
innerLEDs=12
totalLEDs = (innerLEDs+outerLEDs)

cabinetStart=0
cabinetLEDs=30

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
        self.ringStart=ringStart
        self.cabinetStart=cabinetStart
        self.cabinetLEDs=cabinetLEDs
        self.progress=0
        self.savedProgress=(0,0,0)
        
    #Function to call on an image snap
    def onSnap(self,t=0.1):
        pulseIntensity=copy.copy(self.intensity)
        for i in range(self.outerLEDs):
            pulseIntensity[self.ringStart+i]=(self.power,self.power,self.power)
        self.pulseLEDs(pulseIntensity,t)


    def onError(self,t=1.0, repeats=30):
        pulseIntensity=copy.copy(self.intensity)
        for i in range(outerLEDs):
            pulseIntensity[self.ringStart+i]=(self.power,0,0)
        for i in range(repeats):
            self.pulseLEDs(pulseIntensity,t)
            time.sleep(t)

    def setWhite(self):
        for i in range(self.totalLEDs):
            self.intensity[self.ringStart+i]=(self.power,self.power,self.power)
        self.setLEDs(None)

    def setOff(self):
        for i in range(self.totalLEDs):
            self.intensity[self.ringStart+i]=(0,0,0)
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


    def setInner(self,col=(100,100,100)):
        for i in range(self.innerLEDs):
            self.intensity[self.ringStart+self.outerLEDs+i]=(col)
        self.setLEDs(None)

    

    def setOuter(self,col=(100,100,100)):
        for i in range(self.outerLEDs):
            self.intensity[self.ringStart+i]=(col)
        self.setLEDs(None)

    def incProgress(self,col=(0,100,0)):
        self.intensity[self.ringStart+self.progress]=self.savedProgress
        self.progress=self.progress+1
        if self.progress>(self.outerLEDs-1):
            self.progress=0
        self.savedProgress=copy.copy(self.intensity[self.ringStart+self.progress])
        self.intensity[self.ringStart+self.progress]=col
        self.setLEDs(None)

    def stopProgress(self):
        self.intensity[self.ringStart+self.progress]=self.savedProgress
        self.setLEDs(None)


    def cabinetOn(self):
        for i in range(self.cabinetLEDs):
            self.intensity[self.cabinetStart+i]=(255,255,255)
        self.setLEDs(None)

    def cabinetOff(self):
        for i in range(self.cabinetLEDs):
            self.intensity[self.cabinetStart+i]=(0,0,0)
        self.setLEDs(None)


    def demo1(self):
        for i in range(23):
            self.intensity[self.ringStart+i]=(255,0,0)
            self.intensity[self.ringStart+i+1]=(255,0,0)      
            if i%2 == 0:
                self.intensity[self.ringStart+self.outerLEDs+int(i/2)]=(255,0,0)
            else:
                self.intensity[self.ringStart+self.outerLEDs+int(i/2)]=(150,0,0)
                self.intensity[self.ringStart+self.outerLEDs+int(i/2)+1]=(150,0,0)
            self.setLEDs(None)
            time.sleep(1)
            self.intensity[self.ringStart+i]=(100,100,100)
            self.intensity[self.ringStart+i+1]=(100,100,100)
            self.intensity[self.ringStart+self.outerLEDs+int(i/2)]=(100,100,100)
            self.setLEDs(None)


    def demo2(self):
        self.onSnap()
        self.setInner((150,0,0))
        self.incProgress()
        time.sleep(1)
        self.onSnap()
        self.setInner((0,150,0))
        self.incProgress()
        time.sleep(1)
        
