import sys
import numpy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QCheckBox
from soundRecorder import *
from plotDisp import *
from scoreGen import *
from textDisp import *
from volumeSlider import *
from inputPad import *
from metronome import *
from dnn import *
from chord import *


buf = [0]
music = [0]
is_first = True
is_start = False
enable_metro = False
para1 = 0.3
para2 = 0.8

#--------------------------------
#Get data from the sound recorder
#--------------------------------
def getData():
	global buf

	if sr.is_nextWave:
		buf = numpy.concatenate((buf, sr.wave))
		sr.is_nextWave = False

		
#--------------------------------
#Refresh the screen
#--------------------------------
def refresh():
	global buf, music, is_first
	
	if len(buf) > sg.noteInterval*2:
		#Get spectrum from 2048 pts fft
		signal = buf[:sg.points]
		spec = numpy.split(numpy.abs(numpy.fft.fft(signal)), 2)[0] * 0.0001 * vs.slider.value()
		spec[0] = 0
		
		#Find score from DNN (time domain)
		score1 = sg.scoreFromFFT(spec)
		estimateChord = find_chord(score1, para1, para2)
		
		#Find pitch from autocorrelation
		estimatePitch = sg.pitchFromAutocorr(signal)
		
		#Find score from HPS
		score2 = sg.scoreFromHPS(spec)
		
		#Find score from DNN (freq domain)
		feature = scoreDnn.fprop(spec[:512])
		score3 = dnnFold(feature)
		
		#Fuse score1 & score2
		out = complemantary(score2, score3)
		maxIndex = 0
		maxValue = 0
		
		for i in range(12):
			if maxValue < out[i]:
				maxIndex = i
				maxValue = out[i]
		
		#Choose the best estimated score
		if sum(score1) < 0.5:
			music.append('O   ')
		else:
			if estimateChord == 'X  X' or estimatePitch == dnnMax(feature, maxIndex):
				music.append(noteDecode(estimatePitch))
			else:
				music.append(estimateChord)
			
		#Update the screen
		data =  'C : %.2f\n' % (score1[0])
		data += 'C#: %.2f\n' % (score1[1])
		data += 'D : %.2f\n' % (score1[2])
		data += 'D#: %.2f\n' % (score1[3])
		data += 'E : %.2f\n' % (score1[4])
		data += 'F : %.2f\n' % (score1[5])
		data += 'F#: %.2f\n' % (score1[6])
		data += 'G : %.2f\n' % (score1[7])
		data += 'G#: %.2f\n' % (score1[8])
		data += 'A : %.2f\n' % (score1[9])
		data += 'A#: %.2f\n' % (score1[10])
		data += 'B : %.2f\n' % (score1[11])
		
		scoreDisp1.text = data
		
		data =  'C : %.2f\n' % (out[0])
		data += 'C#: %.2f\n' % (out[1])
		data += 'D : %.2f\n' % (out[2])
		data += 'D#: %.2f\n' % (out[3])
		data += 'E : %.2f\n' % (out[4])
		data += 'F : %.2f\n' % (out[5])
		data += 'F#: %.2f\n' % (out[6])
		data += 'G : %.2f\n' % (out[7])
		data += 'G#: %.2f\n' % (out[8])
		data += 'A : %.2f\n' % (out[9])
		data += 'A#: %.2f\n' % (out[10])
		data += 'B : %.2f\n' % (out[11])
		
		scoreDisp2.text = data	

		estimateLabel1.setText(noteDecode(dnnMax(feature, maxIndex)))
		estimateLabel2.setText(noteDecode(estimatePitch))
		estimateLabel3.setText(estimateChord)
		fftDisp.setPointsY(spec)
		fftDisp.update()
		scoreDisp1.update()
		scoreDisp2.update()
		
		#Release data
		if is_first:
			buf = buf[sg.noteInterval - int(sg.points/2) : ]
			is_first = False
		else:
			buf = buf[sg.noteInterval : ]
			

#--------------------------------
#Complemantary of score1 & score2
#--------------------------------
def complemantary(score1, score2):
	tmp = [0]*12
	out = [0]*12
	
	for i in range(12):
		tmp[i] = score1[i] * 0.1 + score2[i] * 0.9
	
	out[0] = tmp[0] * 6 + tmp[1] + tmp[11]
	out[11] = tmp[11] * 6 + tmp[10] + tmp[1]

	for i in range(1, 11):
		out[i] = tmp[i] * 6 + tmp[i-1] + tmp[i+1]
	
	total = sum(out)
		
	if total == 0: return out
	return numpy.divide(out, total)
	
	
#--------------------------------
#Decode into a note
#--------------------------------
def noteDecode(code):
	p = numpy.mod(code, 12)
	
	if   p == 0: note = 'C '
	elif p == 1: note = 'C#'
	elif p == 2: note = 'D '
	elif p == 3: note = 'D#'
	elif p == 4: note = 'E '
	elif p == 5: note = 'F '
	elif p == 6: note = 'F#'
	elif p == 7: note = 'G '
	elif p == 8: note = 'G#'
	elif p == 9: note = 'A '
	elif p == 10: note = 'A#'
	elif p == 11: note = 'B '
	else: note = 'X'
	
	interval = code/12 + 1
	
	return "%2s%2d" % (note, interval)
	
	
#--------------------------------
#Find max from DNN
#--------------------------------
def dnnMax(data, maxIndex):
	if data[maxIndex] < data[maxIndex+12]:
		maxIndex += 12
	
	if data[maxIndex] < data[maxIndex+12]:
		maxIndex += 12
	
	return maxIndex - 12
	

#--------------------------------
#Fold data from DNN
#--------------------------------
def dnnFold(code):
	list = [0] * 12
		
	for i in range(36):
		list[i%12] += code[i]
	
	down = min(list)
	for i in range(12):
		list[i] -= down
	
	sum_list = sum(list)
	for i in range(12):
		list[i] /= sum_list
		
	return list


#--------------------------------
#On start button clicked event
#--------------------------------
def onStartBtnClicked():
	global buf, music, is_first, is_start

	#Stop
	if is_start:
		startBtn.setText('Start')
		sr.is_nextWave = False
		sr.waveClear()
		sr.threadEnd()
		if enable_metro == True: metro.stop()
		is_start = False
		checkBoxMetro.setEnabled(True)
		
	#Start
	else:
		startBtn.setText('Stop')
		buf = []
		music = []
		attack = []
		is_first = True
		sr.threadStart()
		if enable_metro == True: metro.play()
		is_start = True
		checkBoxMetro.setEnabled(False)
		hintLabel.setText('');
		
		
#--------------------------------
#On save button clicked event
#--------------------------------
def onSaveBtnClicked():
	if is_start == False and len(music) > 0:
		fp = open('score.txt', 'w')
		tab = []
		count  = 0
		last = 'O   '
		for item in music:
			if last == item:
				tab.append(item)
			else:
				tab.append('X   ')
			
			last = item
			
		for i in range(len(tab)-2):
			if tab[i] == 'X   ' and tab[i+1] != 'X   ' and tab[i+2] == 'X   ':
				tab[i+1] = 'X   '
		
		last = 'O   '
		
		for i in range(-len(tab), 0):
			if tab[i] == 'X   ':
				tab[i] = last
			else:
				last = tab[i]
				
		count = 0
		note = 'O   '
		
		for item in tab:
			if count == 0:
				count = 1
				note = item
			elif item == note:
				count += 1
			else:
				if count < 3:
					fp.write("%s,%d\n" % (note, 1));
				elif count < 5:
					fp.write("%s,%d\n" % (note, 2));
				elif count < 7:
					fp.write("%s,%d\n" % (note, 3));
				elif count < 11:
					fp.write("%s,%d\n" % (note, 4));
				elif count < 14:
					fp.write("%s,%d\n" % (note, 6));
				elif count < 20:
					fp.write("%s,%d\n" % (note, 8));
				elif count < 29:
					fp.write("%s,%d\n" % (note, 12));
				else:
					fp.write("%s,%d\n" % (note, 16));
				
				count = 1
				note = item
			
		fp.close()
		hintLabel.setText('Saved successfully!');


#--------------------------------
#On input button clicked event
#--------------------------------
def onInputBtnClicked():
	global is_start
	
	#Change BPM
	if is_start == False and bpmInput.inputLine.text() != '':
		bpm = int(bpmInput.inputLine.text())
		
		if bpm <= 200 and bpm >= 60:
			sg.resetBPM(bpm)
			metro.resetBPM(bpm)
			bpmLabel.setText('BPM: ' + str(bpm))
			

#--------------------------------
#On para1 button clicked event
#--------------------------------
def onParaBtnClicked1():
	global para1
	
	if chordInput1.inputLine.text() != '' and float(chordInput1.inputLine.text()) > 0:
		para1 = float(chordInput1.inputLine.text())
		paraLabel1.setText("Para1: %.2f" % (para1));
		

#--------------------------------
#On para2 button clicked event
#--------------------------------
def onParaBtnClicked2():
	global para2
	
	if chordInput2.inputLine.text() != '' and float(chordInput2.inputLine.text()) > 0:
		para2 = float(chordInput2.inputLine.text())
		paraLabel2.setText("Para2: %.2f" % (para2));
		

#--------------------------------
#On metronome checked event
#--------------------------------
def onMetroChecked():
	global enable_metro
	enable_metro = checkBoxMetro.isChecked();
	

if __name__ == "__main__":
	app = QApplication(sys.argv)

	#Create main window
	window = QWidget()
	window.setGeometry(0, 50, 1460, 750)
	window.setWindowTitle('Score Generator')
	
	#Set the background color
	pal = window.palette()
	pal.setColor(window.backgroundRole(), Qt.gray)
	window.setPalette(pal)
	window.setAutoFillBackground(True)
	
	#save button
	saveBtn = QPushButton('Save', window)
	saveBtn.setGeometry(1100, 600, 100, 50)
	saveBtn.clicked.connect(onSaveBtnClicked)
	
	#start button
	startBtn = QPushButton('Start', window)
	startBtn.setGeometry(1100, 540, 100, 50)
	startBtn.clicked.connect(onStartBtnClicked)
	
	#fft plot display
	fftDisp = plotDisp(window, posX = 20)
	fftDisp.setPointsX(numpy.arange(1024, dtype = float))
	fftDisp.setAxis(intervalX = 1000, ratioX = 0.046)
	
	#score display
	scoreDisp1 = textDisp(window, posX = 650, width = 200, height = 400)
	scoreDisp2 = textDisp(window, posX = 870, width = 200, height = 400)
	
	#estimateLabel
	estimateLabel1 = QLabel(window)
	estimateLabel1.setGeometry(870, 420, 170, 120)
	estimateLabel1.setText('')
	estimateLabel1.setStyleSheet('font-size: 40pt; font-family: Courier; color: red;')
	
	estimateLabel2 = QLabel(window)
	estimateLabel2.setGeometry(670, 580, 170, 120)
	estimateLabel2.setText('')
	estimateLabel2.setStyleSheet('font-size: 40pt; font-family: Courier; color: green;')
	
	estimateLabel3 = QLabel(window)
	estimateLabel3.setGeometry(650, 420, 170, 120)
	estimateLabel3.setText('')
	estimateLabel3.setStyleSheet('font-size: 40pt; font-family: Courier; color: red;')
	
	#Hint label
	hintLabel = QLabel(window)
	hintLabel.setGeometry(1000, 650, 300, 50)
	hintLabel.setText('')
	hintLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	#volume slider
	vs = volumeSlider(window, posX = 20, posY = 500, width = 250)
	
	#input pad
	bpmInput = inputPad(window, posX = 350, posY = 500, title = 'BPM:')
	bpmInput.inputLine.setText('120')
	bpmInput.inputBtn.clicked.connect(onInputBtnClicked)
	
	chordInput1 = inputPad(window, posX = 1100, posY = 100, title = 'Para1:')
	chordInput1.inputLine.setText('0.3')
	chordInput1.inputBtn.clicked.connect(onParaBtnClicked1)
	
	chordInput2 = inputPad(window, posX = 1100, posY = 300, title = 'Para2:')
	chordInput2.inputLine.setText('0.8')
	chordInput2.inputBtn.clicked.connect(onParaBtnClicked2)
	
	#bpm label
	bpmLabel = QLabel(window)
	bpmLabel.setGeometry(350, 620, 150, 50)
	bpmLabel.setText('BPM: 120')
	bpmLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	#metronome label
	metroLabel = QLabel(window)
	metroLabel.setGeometry(350, 650, 150, 50)
	metroLabel.setText('Metronome')
	metroLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	#para label
	paraLabel1 = QLabel(window)
	paraLabel1.setGeometry(1100, 220, 200, 50)
	paraLabel1.setText('Para1: 0.30')
	paraLabel1.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	paraLabel2 = QLabel(window)
	paraLabel2.setGeometry(1100, 420, 200, 50)
	paraLabel2.setText('Para2: 0.80')
	paraLabel2.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	#Some labels
	specLabel = QLabel(window)
	specLabel.setGeometry(70, 10, 200, 50)
	specLabel.setText('Spectrum')
	specLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	fftLabel = QLabel(window)
	fftLabel.setGeometry(660, 10, 200, 50)
	fftLabel.setText('FFT')
	fftLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	dnnHpsLabel = QLabel(window)
	dnnHpsLabel.setGeometry(880, 10, 200, 50)
	dnnHpsLabel.setText('DNN + HPS')
	dnnHpsLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: red;')
	
	autocorrLabel = QLabel(window)
	autocorrLabel.setGeometry(650, 550, 300, 50)
	autocorrLabel.setText('Autocorrelation:')
	autocorrLabel.setStyleSheet('font-size: 20pt; font-family: Courier; color: green;')
	
	#metronome check box
	checkBoxMetro = QCheckBox(window)
	checkBoxMetro.setChecked = False
	checkBoxMetro.stateChanged.connect(onMetroChecked)
	checkBoxMetro.setGeometry(320, 650, 50, 50)
	
	#metronome
	metro = metronome('metr.wav')
	
	#score generator
	sg = scoreGen(points = 2048, bpm = 200)
	
	#Deep neural network
	scoreDnn = dnn('freq_train_old.dnn')
	
	#sound recorder
	sr = soundRecorder()
	
	window.show()
	
	#Start the timer for getData function
	timer1 = QtCore.QTimer()
	timer1.timeout.connect(getData)
	timer1.start(1.0)
	
	#Start the timer for refresh function
	timer2 = QtCore.QTimer()
	timer2.timeout.connect(refresh)
	timer2.start(1.0)
	
	code = app.exec()
	sr.threadEnd()
	sr.close()
	sys.exit(code)