#-*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class plotDisp(QWidget):
	def __init__(self, window, posX = 50, posY = 50, width = 600, height = 400):
		super().__init__(window)
		self.setGeometry(posX, posY, width, height)
		
		#Set the background color
		pal = self.palette()
		pal.setColor(self.backgroundRole(), Qt.black)
		self.setPalette(pal)
		self.setAutoFillBackground(True)
		
		#Set pen color
		self.color = Qt.red
		
		self.x = []
		self.y = []
		self.axisX = []
		self.axisY = []
		self.offsetX = 50
		self.offsetY = 50
		self.ratioX = 1
		self.ratioY = 1
		self.width = width
		self.height = height
		
	
	#--------------------------------
	#Set xy points
	#--------------------------------
	def setPoints(self, x, y):
		self.x = [i + self.offsetX for i in x]
		self.y = [self.height - self.offsetY - i for i in y]
	
	
	#--------------------------------
	#Set x points
	#--------------------------------	
	def setPointsX(self, x):
		self.x = [i + self.offsetX for i in x]
	
	
	#--------------------------------
	#Set y points
	#--------------------------------
	def setPointsY(self, y):
		self.y = [self.height - self.offsetY - i for i in y]
	
	
	#--------------------------------
	#Set pen color
	#--------------------------------
	def setColor(self, color):
		self.color = color
		
	
	#--------------------------------
	#Set the axis
	#--------------------------------
	def setAxis(self, intervalX = 50, intervalY = 50, ratioX = 1, ratioY = 1):
		self.axisX = [0]
		self.axisY = [0]
		
		i = 0
		
		while i * ratioX + self.offsetX < self.width:
			i += intervalX
			self.axisX.append(i)
			
		i = 0
		
		while i * ratioY + self.offsetY < self.height:
			i += intervalY
			self.axisY.append(i)
			
		self.ratioX = ratioX
		self.ratioY = ratioY
	
	
	#--------------------------------
	#Re-paint GUI
	#--------------------------------
	def paintEvent(self, e):
		painter = QPainter()
		painter.begin(self)
		painter.setPen(self.color)
		
		self.plot(painter)
		self.plotAxis(painter)
		
		painter.end()
		
	
	#--------------------------------
	#Plot the line chart
	#--------------------------------
	def plot(self, painter):
		if len(self.x) == len(self.y):
			for i in range(len(self.x) - 1):
				painter.drawLine(self.x[i], self.y[i], self.x[i+1], self.y[i+1])
	
	
	#--------------------------------
	#Plot the axis
	#--------------------------------
	def plotAxis(self, painter):
		for x in self.axisX:
			painter.drawText(x * self.ratioX + self.offsetX, self.height - 20, str(x))
			
		for y in self.axisY:
			painter.drawText(0, self.height - y * self.ratioY - self.offsetY, str(y))