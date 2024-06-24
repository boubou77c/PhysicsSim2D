
import sys
import webbrowser

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QDoubleSpinBox,QComboBox,QCommandLinkButton,QRadioButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import uic

import PSEngine

__VERSION__ = "0.1.0"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        #Initialize the window
        self.setFixedSize(1386,712)

        self.action = actionWindow(self)
        self.PhysiqueEngine = PSEngine.PhysiqueSimulator(main_window=self)

        self.initUI()

    def initUI(self):
        #Load the ui
        ui = uic.loadUi('engine.ui', self)
        self.setWindowTitle('Physique Simulator')

        #Get the child
        self.dTimeSB = ui.findChild(QDoubleSpinBox, "dTime")
        self.fricSB = ui.findChild(QDoubleSpinBox, "friction")
        self.ispYSB = ui.findChild(QDoubleSpinBox, "ispY")
        self.ispXSB = ui.findChild(QDoubleSpinBox, "ispX")
        self.gravitySB = ui.findChild(QDoubleSpinBox, "gravity")
        self.restitutionSB = ui.findChild(QDoubleSpinBox, "restitutionSB")

        self.dragRB = ui.findChild(QRadioButton, "drag")


        self.startBtn = ui.findChild(QPushButton, "start")
        self.resetBtn = ui.findChild(QPushButton, "reset")

        self.vbox = ui.findChild(QVBoxLayout, "vbox")

        self.comboBox = ui.findChild(QComboBox, "cbGravity")

        self.link_button = ui.findChild(QCommandLinkButton, "commandLinkButton")

        self.xLabel = ui.findChild(QLabel, "x")
        self.yLabel = ui.findChild(QLabel, "y")
        versionLB = ui.findChild(QLabel, "versionLB")
        versionLB.setText("Version : "+__VERSION__)



        #Add preset gravity for the earth, moon and sun
        self.comboBox.addItem("Earth")
        self.comboBox.addItem("Moon")
        self.comboBox.addItem("Sun")

        #Add the physiqueEngine in the VBOX
        self.vbox.addWidget(self.PhysiqueEngine)

        self.vbox.setAlignment(Qt.AlignCenter)

        self.startBtn.clicked.connect(self.action.start_simulation)
        self.comboBox.currentIndexChanged.connect(self.action.update_gravity)

        self.resetBtn.clicked.connect(self.action.reset_simulation)
        self.link_button.clicked.connect(self.action.open_link)

        self.timer = QTimer()

        self.timer.timeout.connect(self.PhysiqueEngine.update_pos)



class actionWindow:
    def __init__(self,main_window):
        self.main_window = main_window


    #Open my gitHub page
    def open_link(self):
        webbrowser.open("https://github.com/boubou77c")

    #Update the preset gravity
    def update_gravity(self):
        current_text = self.main_window.comboBox.currentText()
        if (current_text == "Earth"):
            self.main_window.gravitySB.setValue(9.8)
        elif (current_text == "Moon"):
            self.main_window.gravitySB.setValue(1.62)
        elif (current_text == "Sun"):
            self.main_window.gravitySB.setValue(274)


    #Update and send the sim setting
    def update_simulation_params(self):

        self.dTimeSBValue = self.main_window.dTimeSB.value()
        self.fricSBValue = self.main_window.fricSB.value()
        self.ispYSBValue = self.main_window.ispYSB.value()
        self.ispXSBValue = self.main_window.ispXSB.value()
        self.restitutionSBValue = self.main_window.restitutionSB.value()
        self.gravitySBValue = self.main_window.gravitySB.value()

        self.main_window.PhysiqueEngine.set_simulation_params(dTime=self.dTimeSBValue, friction=self.fricSBValue,
                                           ispX=self.ispXSBValue, ispY=self.ispYSBValue,gravity=self.gravitySBValue,restitution=self.restitutionSBValue)


    #Start or stop the simulation
    def start_simulation(self):
        if  self.main_window.timer.isActive():
            print("Simulation stoped")
            self.main_window.startBtn.setText("Start")
            self.main_window.timer.stop()
        else:
            print("Simulation started")
            self.update_simulation_params()
            self.main_window.startBtn.setText("Stop")
            self.main_window.timer.start(16)


    #Reset the sim
    def reset_simulation(self):
        print("Reset Simulation")
        self.main_window.PhysiqueEngine.positions.clear()
        self.main_window.timer.stop()

        self.main_window.PhysiqueEngine.x = 1
        self.main_window.PhysiqueEngine.y = 1
        self.main_window.startBtn.setText("Start")

        self.main_window.PhysiqueEngine.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())



