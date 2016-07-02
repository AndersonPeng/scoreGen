#-*- coding: utf-8 -*-

from PyQt5 import QtCore
import pyaudio
import wave
import sys


class metronome():
	def __init__(self, filename, bpm = 120):
		self.bpm = bpm
		self.timeInterval = 60.0/float(bpm) * 1000
		
		#Use pyaudio to play the metronome
		waveFile = wave.open(filename, 'rb')
		p = pyaudio.PyAudio()
		self.outStream = p.open(format = p.get_format_from_width(waveFile.getsampwidth()),
								channels = waveFile.getnchannels(),
								rate = waveFile.getframerate(),
								output = True)
		
		#Only play the audio with length 8192
		self.waveData = waveFile.readframes(8192)
		
		#Set timer for the metronome
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.beat)
	
	
	def resetBPM(self, bpm = 120):
		self.bpm = bpm
		self.timeInterval = 60.0/float(bpm) * 1000
	
	
	def play(self):
		self.outStream.write(self.waveData)
		self.timer.start(self.timeInterval)

	
	def stop(self):
		self.timer.stop()
		
		
	def beat(self):
		self.outStream.write(self.waveData)