#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class textDisp(QWidget):
	def __init__(self, window, posX = 50, posY = 50, width = 100, height = 100):
		super().__init__(window)	
		self.setGeometry(posX, posY, width, height)
		self.setStyleSheet('font-size: 20pt; font-family: Courier;')
		
		#Set the background color
		pal = self.palette()
		pal.setColor(self.backgroundRole(), Qt.black)
		self.setPalette(pal)
		self.setAutoFillBackground(True)
		
		#Set text color
		self.color = Qt.red
		self.text = ''

		
	#------------------------------------
	#Re-paint GUI
	#------------------------------------
	def paintEvent(self, e):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(self.color)
		
		painter.drawText(e.rect(), Qt.AlignLeft, self.text)
		
		painter.end()