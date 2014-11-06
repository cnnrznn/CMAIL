#====================================================
# Author:       Connor Zanin
#
# Description:  This is a helper class to handle
#               email i/o from gmail's imap4 and
#               smtp IMAP_SERVERs
#====================================================

import imaplib,email,smtplib
from email.mime.text import MIMEText

class MailHelper: 

    #
    # CLASS CONSTRUCTOR
    #
    def __init__(self, username, password):
        self.IMAP_SERVER = None
        self.SMTP_SERVER = None
        self.username = username
        self.password = password

    #
    # FUNCTION TO CONNECT TO IMAP_SERVER AND LOGIN
    # @returns boolean to indicate success
    #
    def connect_to_server(self):
        try:
            self.IMAP_SERVER = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.SMTP_SERVER = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            self.IMAP_SERVER.login(self.username, self.password)
            self.SMTP_SERVER.login(self.username, self.password)
            return(True)
        except:
            return(False)

    #
    # FUNCTION TO LOGOUT AND CLOSE CONNECTION
    # @returns boolean to indicate success
    #
    def disconnect_from_server(self):
        if (self.IMAP_SERVER!=None):
            self.IMAP_SERVER.select()
            self.IMAP_SERVER.close()
            self.IMAP_SERVER.logout()
        if (self.SMTP_SERVER!= None):
            self.SMTP_SERVER.quit()

    def DoGetMail(self, num):
	self.IMAP_SERVER.select()
	res, data = self.IMAP_SERVER.uid("SEARCH", None, "ALL")
	uids = data[0].split()
	msgs = []
	for i in range(1,num+1):
		res, data = self.IMAP_SERVER.uid("FETCH", uids[-i], "(BODY[])")
		msg = email.message_from_string(data[0][1])
		msgs.append(msg)
	return(msgs)
