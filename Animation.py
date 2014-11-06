#====================================
# Author: 	Connor Zanin
# Description:	This module will hold static methods
#		to off-load animation logic from 
#		main modules and class logic
#====================================

import curses, time, threading

class Animator :
	
	def __init__(self) :
		self._killthread = False
	
	def ConnectText(self,window,x,y,colorAttr1,colorAttr2):
		self._killthread = False
		m = " Connecting to server "
		x2 = x + len(m)
		ndots = 8
		temp = 0
		tmode = True
		window.addstr(y,x,m,colorAttr1)
		while (not(self._killthread)):
			for i in range(ndots):
				if (tmode):
					if (i < temp):
						window.addstr(y,x2+i,'.',colorAttr1)
					else:
						window.addstr(y,x2+i,'.',colorAttr2)
				else:
					if (i<temp):
						window.addstr(y,x2+i,'.',colorAttr2)
					else:
						window.addstr(y,x2+i,'.',colorAttr1)
			temp += 1
			if (temp > ndots):
				temp = 1
				tmode = not(tmode)
			
			window.noutrefresh()
			curses.doupdate()
			time.sleep(.2)

	# This method will take care of
	# spawning a thread to run
	# the 'connecting to server'
	# text animation
	#
	def BeginConnectText(self, window, x, y,colorAttr1, colorAttr2):
		_killthread = False
		th0 = threading.Thread(target=self.ConnectText, args=(window, x, y, colorAttr1, colorAttr2))
		th0.start()

# This method can be used to draw
# text in a y location that "grows"
# outwards.
#
def OutwardSpawnText(window, x, y, message, colorAttr) :
	bool = False
	temp = ""
	for s in message :
		temp += s
		window.addstr(y, x, temp, colorAttr)
		if (bool) : x -= 1
		bool = not(bool)
		window.noutrefresh()
		curses.doupdate()
		time.sleep(.01)
