#-*- coding: utf-8 -*-

import numpy


class scoreGen:
	def __init__(self, Fs = 44100, points = 1024, bpm = 120, noteScale = 8):
		self.Fs = Fs
		self.bpm = bpm
		self.noteScale = noteScale
		self.noteInterval = int(numpy.round(60/bpm/noteScale * Fs))
		self.freq = []
		self.points = points
		
		for i in range(int(points/2)):
			self.freq.append(i*(Fs/2)/(points/2))
	
	
	#--------------------------------
	#Find peaks from data
	#--------------------------------
	def findPeak(self, data, count = 20, threshold = 20):
		peak_index = []
		peak_value = []
		j = 1
		
		for i in range(len(data)-2):
			tmp = data[i:i+3]
			
			if j < count and tmp[1] > threshold and max(tmp) == tmp[1]:
				peak_index.append(i + 1)
				peak_value.append(data[i + 1])
				j += 1

		return sorted(zip(peak_value, peak_index))
	
	
	#--------------------------------
	#Compute pitch
	#--------------------------------
	def pitch(self, freq):
		fs = freq/261.6255653
		fs = int(numpy.round(numpy.log10(fs) / 0.0250858))
		
		return fs
		
	
	#--------------------------------
	#Compute score from FFT data
	#--------------------------------
	def scoreFromFFT(self, spec):
		score = [0]*12
		peak = self.findPeak(spec, threshold = 5)
		
		for p in peak:
			score[self.pitch(self.freq[p[1]])%12] += p[0]
			
		total = sum(score)
		if total == 0: return score
		return numpy.divide(score, total)
		
	
	#---------------------------------------
	#Estimate the pitch from autocorrelation
	#---------------------------------------
	def pitchFromAutocorr(self, data):
		corr = numpy.convolve(data, data[::-1])
		corr = corr[int(len(corr)/2):]
		peak = self.findPeak(corr)
		
		if len(peak) == 0: return 0
		return self.pitch(self.Fs / peak[-1][1])
	
	
	#---------------------------------------
	#Compute score from HPS
	#---------------------------------------
	def scoreFromHPS(self, spec):
		length = int(len(spec)/4)	
		hps = spec[:length]
		score = [0]*12
		
		for i in range(2, 5):
			tmp = self.downsample(spec, ratio = i)
			hps = numpy.multiply(hps, tmp[:length])
			
		peak = self.findPeak(hps, threshold = 5)
		
		for p in peak:
			score[self.pitch(self.freq[p[1]])%12] += p[0]
			
		total = sum(score)
		if total == 0: return score
		return numpy.divide(score, total)

	
	#---------------------------------------
	#Down sample the data
	#---------------------------------------
	def downsample(self, data, ratio = 1):
		length = int(len(data)/ratio)
		output = [0]*length
		
		for i in range(length):
			output[i] = data[i*ratio]
		
		return output

		
	#---------------------------------------
	#Reset BPM
	#---------------------------------------
	def resetBPM(self, bpm = 120):
		self.bpm = bpm
		self.noteInterval = int(numpy.round(60/bpm/self.noteScale * self.Fs))