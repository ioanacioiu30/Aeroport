import sys
from random import randint
from Plane import Plane
import time
from math import trunc
#from queue import PriorityQueue
from ModelImpl import *
import re
import operator
import os
import sys 
from PyQt4 import QtCore
from PyQt4.QtCore import QObject, pyqtSignal
from radar import Ui_RadarWidget
list_of_names = ['Burkina Air', 'TAROM', 'MoldAir', 'Aeroflot']

class Simulation2(QObject, Ui_RadarWidget):

	header = ['Nume', 'Prioritate', 'Timp Estimat']
	def __init__(self, maxNumber, timerTick, numPiste):
		super(Simulation2, self).__init__()
		self.running = 0
		self.currentNumber = 0
		self.maxNumber = maxNumber
		self.timerTick = timerTick
		self.listOfAirplanes = numPiste * [None]
		self.numPiste = numPiste
		self.sosiriIn = []
		self.plecariIn = []
		self.plecariModel = None
		self.sosiriModel = None
		self.__generateInitialData(self.maxNumber)
		self.timer = QTimer()
	def __setTimerTick(self, time):
		self.timerTick = (int)((100 - time) / 50 * 1000)
		self.timer.setInterval(self.timerTick)
		self.setRunning()
	def __generateInitialData(self, nr):
		toGenerate = randint(0, nr)
		self.currentNumber += toGenerate
		print('Generating... ' + str(toGenerate))
		if self.plecariModel is not None:
			self.plecariModel.triggerDataChanging()
			self.sosiriModel.triggerDataChanging()
			

		for i in range(0, toGenerate):
			plane = Plane.generateRandomPlane()
			if plane.status == 0:
				self.plecariIn.append(plane)
			else:
				self.sosiriIn.append(plane)
		self.plecariIn.sort()
		self.sosiriIn.sort()
		if self.plecariModel is not None:
			self.plecariModel.triggerDataChanged()
			self.sosiriModel.triggerDataChanged()
		
		
	def __bindUiToModel(self):
		if self is not None:
			for i in range(self.numPiste):
				airplane = self.listOfAirplanes[i]
				if airplane is not None:
					getattr(self, 'runway' + str(i)).setValue(int(airplane.getPercentage() * 100))
					getattr(self, 'rwplane' + str(i)).setText(airplane.name + ' - ' + airplane.getReadableStatus())
				else:
					getattr(self, 'runway' + str(i)).setValue(0)
					getattr(self, 'rwplane' + str(i)).setText('Libera')
			self.labelSosiri.setText('Sosiri ' + str(len(self.sosiriIn)))
			self.labelPlecari.setText('Plecari ' + str(len(self.plecariIn)))

	def setGraphicalModel(self):
		#self.ui = ui
		self.plecariModel = MyTableModel(self.plecariIn, Simulation2.header,['name', 'priority', 'takeOffTime'],  self.tabelPlecari) 
		self.sosiriModel = MyTableModel(self.sosiriIn,  Simulation2.header,['name', 'priority', 'landingTime'], self.tabelSosiri) 
		self.tabelPlecari.setModel(self.plecariModel)
		self.tabelSosiri.setModel(self.sosiriModel)
		self.__bindUiToModel()
		self.buttonStart.clicked.connect(self.setRunning)
		self.buttonStop.clicked.connect(self.setStopped)
		self.horizontalSlider.valueChanged[int].connect(self.__setTimerTick)
	def setStopped(self):
		self.running = 2
	def setRunning(self):
		self.running = 1
		# Connect it to f
		if not self.timer.isActive():
			self.timer.timeout.connect(self.__runSimulation)
		# Call f() every 1 seconds
			self.timer.start(self.timerTick)

	def __consumePlane(self):
		freeSpots = [x for x in self.listOfAirplanes if x is None]
		numPlanes = len(freeSpots)
		for x in range(numPlanes):
			if len(freeSpots) > 0:
				index = self.listOfAirplanes.index(None)
			else:
				return
			if len(self.plecariIn) > 0:
				depPlane = self.plecariIn[0]
			else:
				depPlane = None
			if len(self.sosiriIn) > 0:
				arrPlane = self.sosiriIn[0]
			else:
				arrPlane = None
			if (arrPlane is None and depPlane is None):
				return
			if arrPlane is None or (depPlane is not None and depPlane.priority < arrPlane.priority):
				self.listOfAirplanes[index] = depPlane
				self.plecariIn.pop(0)
			elif depPlane is None or (arrPlane is not None and depPlane.priority > arrPlane.priority):
				self.listOfAirplanes[index] = arrPlane
				self.sosiriIn.pop(0)
			else:
				if len(self.sosiriIn) > len(self.plecariIn):
					self.listOfAirplanes[index] = arrPlane
					self.sosiriIn.pop(0)
				else:
					self.listOfAirplanes[index] = arrPlane
					self.plecariIn.pop(0)
	def __checkForCompletion(self):
		for i in range(0, len(self.listOfAirplanes)):
			if self.listOfAirplanes[i] is not None:
				if self.listOfAirplanes[i].status == 0:
					self.listOfAirplanes[i].landingTime-=1
				else:
					self.listOfAirplanes[i].takeOffTime-=1
				if self.listOfAirplanes[i].takeOffTime <= 0 or self.listOfAirplanes[i].landingTime<=0:
					self.listOfAirplanes[i] = None
					
	def __runSimulation(self):
		print('Sim time is ' + str(self.timerTick))
		if self.running != 0:
			self.currentNumber = len(self.sosiriIn) + len(self.plecariIn)
			if self.running == 2:
				return
			self.__generateInitialData(self.maxNumber - self.currentNumber)
			self.__checkForCompletion()
			self.__consumePlane()
			self.__printModel()
			self.__bindUiToModel()
		else:
			timer.stop()
	def stopInit(self):
		self.running = 0
	def __printModel(self):
		for i in range(0, len(self.listOfAirplanes)):
			if self.listOfAirplanes[i] is not None:
				print ('RW:' + str(i) + ' --- ' + self.listOfAirplanes[i].name + ' --- ' + str(int(self.listOfAirplanes[i].getPercentage() * 100)) + '%')
			else:
				print ('RW:' + str(i) + ' --- is free')

