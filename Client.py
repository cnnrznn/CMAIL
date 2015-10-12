#====================================
# Author: 	Connor Zanin
# Description:	(todo) make a description
#====================================

import curses, time
import Animation, Mode
from MailHelper import MailHelper

# global color pair numbers
cpf = 1
cpb = 2
cpr = 3
cpv = 4

class Client :

	def init(self) :
		self.cont = None
		self.username = None
		self.password = None
		self.animator = Animation.Animator()
		self.mode = Mode.login
		self.win = curses.initscr()
		self.width = self.win.getmaxyx()[1]
		self.height = self.win.getmaxyx()[0]
		self.loginwin = curses.newwin(11, 50, int(self.height/2-5), int(self.width/2-25))
		self.prevwin = curses.newwin(self.height-2, int(self.width/3), 1, 1)
		self.messwin = curses.newwin(self.height-2, int(self.width-(self.width/3)-3), 1, int(self.width/3+2))
		curses.noecho()
		curses.raw()
		curses.curs_set(0)
		curses.start_color()
		curses.init_pair(cpf, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(cpb, curses.COLOR_BLACK, curses.COLOR_CYAN)
		curses.init_pair(cpr, curses.COLOR_RED, curses.COLOR_BLACK) 
		curses.init_pair(cpv, curses.COLOR_BLACK, curses.COLOR_WHITE)
	
	def Go(self) :
		self.init()
		self.DoSplashScreen()
		curses.flushinp()
		self.win.getch()
		self.DoMainLoop()
		curses.flushinp()
		self.Stop()

	def Stop(self) :
		self.win.erase()
                x = int(self.width/2)
                y = int(self.height/2)
                m = "Program Terminated: Press any key to finish."
                Animation.OutwardSpawnText(self.win, x, y, m, curses.color_pair(cpr))
		self.win.getch()
		curses.endwin()
		# (todo) put other cleanup here

	def DoSplashScreen(self):
		self.DoResetWin()
		x = int(self.width/2)
                y = int(self.height/2-1)
		m = "  Welcome to CMAIL!  "
		Animation.OutwardSpawnText(self.win, x, y, m, curses.color_pair(cpb))
		m = " Press any key to continue... "
		Animation.OutwardSpawnText(self.win, x, y+2, m, curses.color_pair(cpb))

	def DoMainLoop(self) :
		self.DoResetWin()
		self.cont = True
		while (self.cont):
			if (self.mode == Mode.login):
				self.DoLogin()
			elif (self.mode == Mode.connect):
				self.DoConnect()
			elif (self.mode == Mode.inbox):
				self.DoRead()

	def DoMakeBorder(self, window, colorAttr) :
		window.attron(colorAttr)
		window.box()
		window.attroff(colorAttr)

	def DoResetWin(self) :	
		self.win.erase()
		self.DoMakeBorder(self.win, curses.color_pair(cpf))
		self.win.addstr(self.height-1, 2, " Zanin Software ", curses.color_pair(cpr))
		self.DoRefreshWin(self.win)

	def DoRefreshWin(self, window) :
		window.noutrefresh()
		curses.doupdate()

	def DoLogin(self) :
		self.DoResetWin()
		curses.curs_set(2)
		self.username = ""
		self.password = ""
		loginmode = Mode.login_username
		logincont = True
		while (logincont):
			self.DoRenderLogin(self.username, self.password, loginmode)
			c = self.loginwin.getch()
			if (c == 127):
				if (loginmode == Mode.login_username):
					self.username = self.username[:-1]
				else:
					self.password = self.password[:-1]
			elif (c == 10):
				if (loginmode == Mode.login_username):
					loginmode = Mode.login_password
				else:
					self.mode = Mode.connect
					logincont = False	
					if (self.username == "exit"):
						self.cont = False
			elif (c == 27):
				c = self.loginwin.getch()
				c = self.loginwin.getch()
				if (c == 65):
					loginmode = Mode.login_username
				elif (c == 66):
					loginmode = Mode.login_password
			else:
				curses.ungetch(c)
				c = self.win.getkey()
				if (loginmode == Mode.login_username and len(self.username) < 35):
					self.username += c
				elif (loginmode == Mode.login_password and len(self.password) < 35):
					self.password += c

	def DoRenderLogin(self, userarr, passarr, mode) :
		self.loginwin.erase()
		self.DoMakeBorder(self.loginwin, curses.color_pair(cpf))
		self.loginwin.addstr(0,1, " Login ")
		if (mode == Mode.login_username):
			self.loginwin.addstr(4,1, " Username:", curses.color_pair(cpb))
			self.loginwin.addstr(6,1, " Password:", curses.color_pair(cpf))
		else:
			self.loginwin.addstr(4,1, " Username:", curses.color_pair(cpf))
			self.loginwin.addstr(6,1, " Password:", curses.color_pair(cpb))
		tempx = 13
		for c in userarr:
			self.loginwin.addstr(4,tempx,c)
			tempx += 1
		tempx2 = 13
		for c in passarr:
			self.loginwin.addstr(6,tempx2,'*')
			tempx2 += 1
		if (mode == Mode.login_username):
			self.loginwin.move(4, tempx)
		else:
			self.loginwin.move(6, tempx2)
		self.DoRefreshWin(self.loginwin)

	def DoConnect(self) :
		curses.curs_set(0)
		self.animator.BeginConnectText(self.loginwin,1,self.loginwin.getmaxyx()[0]-2,curses.color_pair(cpf),curses.color_pair(cpr))
		self.mailbox = MailHelper(self.username, self.password)
		if (self.mailbox.connect_to_server()):
			self.mode = Mode.inbox
		else:
			# (todo) warn the user of invalid login / network problem
			self.mode = Mode.login
		self.animator._killthread = True

	def DoRead(self) :
		self.DoResetWin()
		self.win.attron(curses.color_pair(cpf))
		self.win.vline(1, int(self.width/3+1), curses.ACS_VLINE, self.height-2)
		self.win.attroff(curses.color_pair(cpf))
		self.DoRefreshWin(self.win)
		num_messages = 20
		msgs = self.mailbox.DoGetMail(num_messages)
		selected = 0
		start = 0
		readcont = True
		while (readcont):
			temp_num = self.DoRenderRead(msgs, start, selected)
			c = self.prevwin.getch()
			if (c == ord('q')):
				self.mode = Mode.login
				readcont = False
			elif (c == 27):
				c = self.prevwin.getch()
				c = self.prevwin.getch()
				if (c == 65 and selected > 0):
					if (selected == start+1 and start > 0):
						start -= 1
					selected -= 1
				elif (c == 66 and selected < len(msgs)-1):
					if (selected > temp_num-2):
						start += 2
					selected += 1

	def DoRenderRead(self, msgs, start, selected):
		self.prevwin.erase()
		self.messwin.erase()
		ct = start
		pl = 1
		try:
			for i in range(start, len(msgs)):
				m = msgs[i]["Subject"].replace('\n','').replace('\r','')
				if (i == selected):
					self.prevwin.addstr(pl, 0, str(ct+1) + ": " + m, curses.color_pair(cpv))
				else:
					self.prevwin.addstr(pl, 0, str(ct+1) + ": " + m)
				ct += 1
				pl += 2
				pl += int((len(m)+3)/(self.width/3))
		except:
			pass
		self.DoDisplayMess(msgs[selected])
		self.DoRefreshWin(self.prevwin)
		self.DoRefreshWin(self.messwin)
		return(ct)

	def DoDisplayMess(self, msg):
		self.messwin.addstr(0,0,"From: " + msg["From"]) 
		self.messwin.addstr(1,0,"Date: " + msg["Date"])
		if (msg.is_multipart()):
			for m in msg.get_payload():
				if (m.get_content_type() == "text/plain"):
					msg = m
					break
		try:
			s = msg.get_payload().replace('\r','')
			self.messwin.addstr(3,0,s)
		except:
			pass

	def DoRenderLegend(self, mode) :
		# (todo) render a legend 
		#	 based on the current mode
		pass
