#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class volumeSlider(QWidget):
	def __init__(self, window, posX = 50, posY = 50, width = 300, height = 100):
		super().__init__(window)
		self.setGeometry(posX, posY, width, height)
		
		#Set the background color
		pal = self.palette()
		pal.setColor(self.backgroundRole(), Qt.black)
		self.setPalette(pal)
		self.setAutoFillBackground(True)
		
		#Create a QLabel
		self.valueLabel = QLabel()
		self.valueLabel.setText('Volume: 50')
		self.valueLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
		
		#Create a QSlider
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMinimum(0)
		self.slider.setMaximum(100)
		self.slider.setValue(50)
		self.slider.setTickPosition(QSlider.TicksBelow)
		self.slider.setTickInterval(10)
		self.slider.valueChanged.connect(self.onValueChanged)
		
		#Set layout
		layout = QVBoxLayout()
		layout.addWidget(self.valueLabel)
		layout.addWidget(self.slider)
		self.setLayout(layout)
	
	
	#------------------------------------
	#On value changed event
	#------------------------------------
	def onValueChanged(self):
		self.valueLabel.setText("Volume: " + str(self.slider.value()))