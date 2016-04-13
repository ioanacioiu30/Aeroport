import re
import operator
import os
import sys 
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
import sys
from random import randint
from Plane import Plane
import time
#from queue import PriorityQueue
import ModelImpl 
import re
import operator
import os
import sys 
from PyQt4 import QtCore
from PyQt4.QtCore import QObject, pyqtSignal
from radar import Ui_RadarWidget
list_of_names = ['Burkina Air', 'TAROM', 'MoldAir', 'Aeroflot']

class Simulation(QObject):
	
	tick=4*[QtCore.pyqtSignal(int, name="changed")]
	header = ['Nume', 'Prioritate']
	def __init__(self, maxNumber, timerTick, numPiste):
		super(Simulation, self).__init__()
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
		self.ui = None
		
	def __generateInitialData(self, nr):
		toGenerate = randint(0, nr)
		self.currentNumber += toGenerate
		if self.plecariModel is not None:
			self.plecariModel.triggerDataChanging()
			self.sosiriModel.triggerDataChanging()
			

		for i in range(1, toGenerate):
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
		if self.ui is not None:
			for i in range(self.numPiste):
				airplane = self.listOfAirplanes[i]
				if airplane is not None:
					getattr(self.ui, 'runway' + str(i)).setValue(int(airplane.getPercentage() * 100))
				else:
					getattr(self.ui, 'runway' + str(i)).setValue(0)
			self.ui.labelSosiri.setText(self.ui.labelSosiri.text() + ' ' + str(len(self.sosiriIn)))
			self.ui.labelPlecari.setText(self.ui.labelPlecari.text() + ' ' + str(len(self.plecariIn)))

	def setGraphicalModel(self, ui):
		self.ui = ui
		self.plecariModel = MyTableModel(self.plecariIn, Simulation.header,['name', 'priority'],  ui.tabelPlecari) 
		self.sosiriModel = MyTableModel(self.sosiriIn,  Simulation.header,['name', 'priority'], ui.tabelSosiri) 
		ui.tabelPlecari.setModel(self.plecariModel)
		ui.tabelSosiri.setModel(self.sosiriModel)
#		for i in range(self.numPiste):
#			tick[i].connect(getattr(self.ui, 'runway' + str(i)).setValue)
		self.__bindUiToModel()
		self.ui.buttonStart.clicked.connect(self.setRunning)
		self.ui.buttonStop.clicked.connect(self.setStopped)
	def setStopped(self):
		self.running = 2
	def setRunning(self):
		self.running = 1
	def startInit(self):
		self.running = 2
		self.__runSimulation()
	def __consumePlane(self):
		freeSpots = [x for x in self.listOfAirplanes if x is None]
		if len(freeSpots) > 0:
			index = self.listOfAirplanes.index(None)
		else:
			return
		print('Free spot at ' + str(index))
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
				print(str(arrPlane) + ' departing from ' + str(index))
			else:
				self.listOfAirplanes[index] = arrPlane
				self.plecariIn.pop(0)
				print(str(arrPlane) + ' arriving on ' + str(index))
	def __checkForCompletion(self):
		for i in range(0, len(self.listOfAirplanes)):
			if self.listOfAirplanes[i] is not None:
				if self.listOfAirplanes[i].status == 0:
					self.listOfAirplanes[i].landingTime-=1
				else:
					self.listOfAirplanes[i].takeOffTime-=1
				if self.listOfAirplanes[i].takeOffTime <= 0 or self.listOfAirplanes[i].landingTime<=0:
					print(str(self.listOfAirplanes[i]) + ' over for rw ' + str(i))
					self.listOfAirplanes[i] = None
					
	def __runSimulation(self):
		while self.running != 0:
			if self.running == 2:
				continue
			if (self.currentNumber < self.maxNumber):
				self.__generateInitialData(self.maxNumber - self.currentNumber)
			self.__checkForCompletion()
			self.__consumePlane()
			self.__printModel()
			time.sleep(self.timerTick)
	def stopInit(self):
		self.running = 0
	def __printModel(self):
		for i in range(0, len(self.listOfAirplanes)):
			if self.listOfAirplanes[i] is not None:
				print ('RW:' + str(i) + ' --- ' + self.listOfAirplanes[i].name + ' --- ' + str(int(self.listOfAirplanes[i].getPercentage() * 100)) + '%')
			else:
				print ('RW:' + str(i) + ' --- is free')

