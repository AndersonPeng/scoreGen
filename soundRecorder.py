#-*- coding: utf-8 -*-

import numpy
import pyaudio
import threading


class soundRecorder:
	def __init__(self, Fs = 44100, bufSize = 1024, bufCount = 2):
		self.is_threadEnd = False
		self.is_nextWave = False
		self.Fs = Fs
		self.bufSize = bufSize
		self.bufCount = bufCount
		self.wave = numpy.empty(bufSize*bufCount, dtype = numpy.int16)
		
		#initialize audio input stream
		self.p = pyaudio.PyAudio()
		self.inStream = self.p.open(format = pyaudio.paInt16,
									channels = 1,
									rate = self.Fs,
									input = True,
									frames_per_buffer = self.bufSize)
	
	
	#------------------------------------
	#Close the input stream
	#------------------------------------
	def close(self):
		self.p.close(self.inStream)
	
	
	#------------------------------------
	#Get wave data
	#------------------------------------
	def getWave(self):
		try:
			waveString = self.inStream.read(self.bufSize)
			return numpy.fromstring(waveString, dtype = numpy.int16)
		except:
			return [0] * self.bufSize
	
	
	#------------------------------------
	#Record wave data
	#------------------------------------
	def record(self):
		while self.is_threadEnd == False:
			for i in range(self.bufCount):
				if self.is_threadEnd == False:
					self.wave[i*self.bufSize : (i+1)*self.bufSize] = self.getWave()
				else: break
				
			self.is_nextWave = True
			
	
	#------------------------------------
	#Clear wave data
	#------------------------------------
	def waveClear(self):
		self.wave = []
	
	
	#------------------------------------
	#Start a thread for recording
	#------------------------------------
	def threadStart(self):
		self.is_threadEnd = False
		t = threading.Thread(target = self.record)
		t.daemon = True
		t.start()
		
		
	#------------------------------------
	#Close the thread
	#------------------------------------
	def threadEnd(self):
		self.is_threadEnd = True