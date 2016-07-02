#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class inputPad(QWidget):
	def __init__(self, window, posX = 50, posY = 50, width = 250, height = 125, title = 'input:'):
		super().__init__(window)
		self.setGeometry(posX, posY, width, height)
		
		#Set the background color
		pal = self.palette()
		pal.setColor(self.backgroundRole(), Qt.black)
		self.setPalette(pal)
		self.setAutoFillBackground(True)
		
		#Create a QLabel
		self.titleLabel = QLabel(self)
		self.titleLabel.setText(title)
		self.titleLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
		
		#Create a QLineEdit
		self.inputLine = QLineEdit(self)
		self.inputLine.setGeometry(10, 50, 100, 50)
		self.inputLine.setStyleSheet('font-size: 20pt; font-family: Courier;')
		
		#Create a QPushButton
		self.inputBtn = QPushButton('Set', self)
		self.inputBtn.setGeometry(130, 50, 100, 50)