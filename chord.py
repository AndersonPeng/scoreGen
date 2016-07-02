#Written by JerryWiston
#The function returns the estimated chord if a chord is found
def find_chord(clist, par1, par2):
	
	for i in range(12):
		ch1 = i
		ch2 = (i+4)%12
		ch3 = (i+7)%12
		
		count = 0
		chord = 0
		sign = 'X'
		
		if clist[ch1] >= par1 and clist[ch1]<0.5:
			count = count + 1
		if clist[ch2] >= par1 and clist[ch2]<0.5 :
			count = count + 1
		if clist[ch3] >= par1 and clist[ch3]<0.5 :
			count = count + 1
		
		if count>=2 and clist[ch1]+clist[ch2]+clist[ch3]>=par2 :
			chord = i
			sign = 'M'
			return "%d  %c" %(chord,sign)
		
		count = 0
		ch2 = (i+3)%12
		
		if clist[ch1] >= par1 and clist[ch1]<0.5 :
			count = count + 1
		if clist[ch2] >= par1 and clist[ch2]<0.5 :
			count = count + 1
		if clist[ch3] >= par1 and clist[ch3]<0.5 :
			count = count + 1
		
		if count>=2 and clist[ch1]+clist[ch2]+clist[ch3]>=par2 :
			chord = i
			sign = 'm'
			return "%d  %c" %(chord,sign)
	
	return "X  X"