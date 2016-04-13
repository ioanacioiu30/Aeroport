import sys
from PyQt4.QtGui import QApplication, QWidget
from radar import Ui_RadarWidget
import ModelImpl
from math import trunc

from Simulation import Simulation
from threading import Thread
from Simulation2 import Simulation2
app = QApplication(sys.argv)
window = QWidget()
ui = Simulation2(10, 1000, 4)
ui.setupUi(window)

datain=[]


#plecariIn = []
#sosiriIn = []

#for i in range(0, 20):
#	plane = Plane.generateRandomPlane()
#	listOfStrings = [plane.name, plane.priority]
#	if plane.status == 0:
##	else:
	#	sosiriIn.append(plane)

#ui.tabelPlecari.setModel(plecariModel)
#ui.tabelSosiri.setModel(sosiriModel)
#ui.labelSosiri.setText(ui.labelSosiri.text() + ' ' + str(len(sosiriIn)))
#ui.labelPlecari.setText(ui.labelPlecari.text() + ' ' + str(len(plecariIn)))



#sim=Simulation(10, 1, 4)
ui.setGraphicalModel()
#thread = Thread(target = ui.startInit)
#thread.start()
app.aboutToQuit.connect(ui.stopInit)
window.show()
sys.exit(app.exec_())
