import sys
from random import randint

list_of_names = ['Burkina Air', 'TAROM', 'MoldAir', 'Aeroflot']

class Plane:
	def __str__(self):
		return self.name + '\n' + str(self.landingTime) + '\n' + str(self.takeOffTime) + '\n' + ('Decoleaza' if self.status == 0 else 'Aterizeaza') + '\nPrioritate:' + str(self.priority)
	def __init__(self, name, landingTime, takeOffTime):
		self.name = name
		self.landingTime = landingTime
		self.__maxLandingTime = landingTime
		self.takeOffTime = takeOffTime
	def getPercentage(self):
		if self.status == 0:
			return (self.__maxLandingTime - self.landingTime) /float( self.__maxLandingTime);
		return (self.__maxLandingTime - self.takeOffTime) / float(self.__maxLandingTime);
	def __lt__(self, other):
		return (self.priority < other.priority)
	def setPriority(self, priority):
		self.priority = priority
	def setName(self, name):
		self.name = name
	def getName(self):
		return self.name
	def setStatus(self, status):
		self.status = status
	def getStatus(self, status):
		return self.status
	def getReadableStatus(self):
		return 'Decoleaza' if self.status == 0 else 'Aterizeaza'
	def generateRandomPlane():
		index = randint(0, len(list_of_names) - 1)
		id = randint(0, 2839)
		landingTime = randint(1, 10)
		plane = Plane(list_of_names[index] + str(id), landingTime, landingTime)
		plane.setStatus(id % 2)
		plane.setPriority(int(randint(0, 60) / 20))
		return plane
	generateRandomPlane = staticmethod(generateRandomPlane)

