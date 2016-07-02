#Written by JerryWiston
#Deep neural network for estimating the score
import numpy as np

class dnn:
	def __init__(self, filename):
		self.total_layer = 0
		self.type = 0
		self.learn_rate = 0.0
		self.wei_decay = 0.0
		self.sparse_wei = 0.0
		self.sparse_par = 0.0
		self.layer = []

		self.wei = []
		self.r_wei = []
		self.bias = []
		self.r_bias = []

		self.c_in = 0
		self.c_hid = 0
		self.c_out = 0
		self.c_wei_in_hid = np.matrix
		self.c_bias_in_hid = np.matrix
		self.c_wei_hid_out = np.matrix
		self.c_bias_hid_out = np.matrix
		self.dnn_read(filename)
		
	def dnn_read(self, filename):
		fp = open(filename,'r')
		wdata = fp.read()
		sdata = wdata.split()
		fptr = 0
		#total_layer
		count = 0
		self.total_layer = int(sdata[fptr])
		fptr = fptr + 1

		#actfun_type
		self.type = int(sdata[fptr])
		fptr = fptr + 1

		#learn_rate
		self.learn_rate = float(sdata[fptr])
		fptr = fptr + 1
		
		#weight_decay
		self.wei_decay = float(sdata[fptr])
		fptr = fptr + 1
		
		#sparse_weight
		self.sparse_wei = float(sdata[fptr])
		fptr = fptr + 1
		
		#sparse_parameter
		self.sparse_par = float(sdata[fptr])
		fptr = fptr + 1
		
		#read_layer
		self.layer = [0]*self.total_layer
		for i in range(self.total_layer):
			self.layer[i] = int(sdata[fptr])
			fptr = fptr + 1
		
		#read_weight
		for k in range(self.total_layer-1):
			#weight
			wei_mid =  np.zeros((self.layer[k+1],self.layer[k]),dtype = float)
			for j in range(self.layer[k+1]):
				for i in range(self.layer[k]):
					wei_mid[j][i] = float(sdata[fptr])
					fptr = fptr + 1
			self.wei.append(wei_mid)
			
			#bias
			bias_mid = np.zeros((self.layer[k+1],1),dtype = float)
			for i in range(self.layer[k+1]):
				bias_mid[i][0] = float(sdata[fptr])
				fptr = fptr + 1
			self.bias.append(bias_mid)
			
			#r_weight
			r_wei_mid =  np.zeros((self.layer[k],self.layer[k+1]),dtype = float)
			for j in range(self.layer[k]):
				for i in range(self.layer[k+1]): 
					r_wei_mid[j][i] = float(sdata[fptr])
					fptr = fptr + 1
			self.r_wei.append(r_wei_mid)
			
			#r_bias
			r_bias_mid = np.zeros((self.layer[k],1),dtype = float)
			for i in range(self.layer[k]): 
				r_bias_mid[i][0] = float(sdata[fptr])
				fptr = fptr + 1
			self.r_bias.append(r_bias_mid)
		
		#read_classifier
		self.c_in = int(sdata[fptr])
		fptr = fptr + 1
		self.c_hid = int(sdata[fptr])
		fptr = fptr + 1
		self.c_out = int(sdata[fptr])
		fptr = fptr + 1
		
		self.c_wei_in_hid =  np.zeros((self.c_hid,self.c_in),dtype = float)
		for j in range(self.c_hid):
			for i in range(self.c_in):
				self.c_wei_in_hid[j][i] = float(sdata[fptr])
				fptr = fptr + 1
		
		self.c_bias_in_hid = np.zeros((self.c_hid,1),dtype = float)
		for i in range(self.c_hid):
			self.c_bias_in_hid[i][0] = float(sdata[fptr])
			fptr = fptr + 1
		
		self.c_wei_hid_out =  np.zeros((self.c_out,self.c_hid),dtype = float)
		for j in range(self.c_out):
			for i in range(self.c_hid):
				self.c_wei_hid_out[j][i] = float(sdata[fptr])
				fptr = fptr + 1

		self.c_bias_hid_out = np.zeros((self.c_out,1),dtype = float)
		for i in range(self.c_out):
			self.c_bias_hid_out[i][0] = float(sdata[fptr])
			fptr = fptr + 1
	
	def actfunc(self, x):
		if self.type == 0 :
			return 1/(1 + np.exp(-1*x))
		elif self.type == 1 :
			return np.tanh(x*2/3)
		elif self.type == 2 :
			return 1.7159 * np.tanh(x*2/3)
		
	def fprop(self, input):
		net1 = np.matrix(input).transpose()
		for j in range(1, self.total_layer):
			net2 = np.dot(self.wei[j-1], net1) + self.bias[j-1]
			for i in range(self.layer[j]):
				net2[i] = self.actfunc(net2[i])
			net1 = net2
	
		net2 = np.dot(self.c_wei_in_hid, net1) + self.c_bias_in_hid
		for i in range(self.c_hid):
			net2[i] = self.actfunc(net2[i])
		net1 = net2
		
		net2 = np.dot(self.c_wei_hid_out, net1) + self.c_bias_hid_out
		for i in range(self.c_out):
			net2[i] = self.actfunc(net2[i])
		net1 = net2
		
		return net1.transpose().tolist()[0]