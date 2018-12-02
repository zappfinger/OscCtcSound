

from pythonosc import dispatcher
from pythonosc import osc_server, udp_client
import time, random

"""
converted to use Python 3.x and python-osc
14-10-2018
"""

class oscy(object):
	def __init__(self, ipport=('127.0.0.1', 9090), address='/midi', address2='/instr2'):
		self.send_address = ipport
		self.address = address
		self.address2 = address2
		self.c = udp_client.SimpleUDPClient(ipport[0], ipport[1])

	def send(self):
		# single message
		self.msg = []
		self.msg.append(self.address) # set OSC address
		self.msg.append(44) # int
		self.msg.append(4.5233) # float
		self.msg.append( "the white cliffs of dover" ) # string
		print(self.msg)
		self.c.send_message(self.msg[0], self.msg[1:]) # send it!

	def sendmidi(self, midilist):
		# single message
		self.msg = []
		self.msg.append(self.address) # set OSC address
		for mi in midilist:
			self.msg.append(mi) # int
		self.c.send_message(self.msg[0], self.msg[1:]) # send it!

	def sendeventlist(self, eventlist):
		# single message
		self.msg = []
		self.msg.append(self.address2) # set OSC address to event
		for ev in eventlist:
			print(ev)
			self.msg.append(ev) # string
		self.c.send_message(self.msg[0], self.msg[1:]) # send it!

	def sendevent(self, event):
		# single message
		self.msg = []
		self.msg.append(self.address2) # set OSC address to event
		self.msg.append(event) # string
		print(event)
		self.c.send_message(self.msg[0], self.msg[1:]) # send it!

if __name__ == '__main__':
	event = 1
	osc = oscy()
	#osc.send()
	try:
		if not event:
			while 1:
				osc.sendmidi([144, 9, 60, 100])
				time.sleep(.2)
				osc.sendmidi([144, 9, 60, 0])
				time.sleep(.8)
		else:
			with open('./scores/Rock3.sco') as f:
				lines = f.readlines()
			#osc.sendevent(['i 12 0 1 100 60\ni 12 0 1 100 64\ni 12 0 1 100 67'])
			for line in lines:
				osc.sendevent(line)

			#osc.sendevent(['i 12 0 1 100 60','i 12 0 2 100 64','i 12 0 3 100 67'])
			#osc.sendevent(['i 11 0 1 100 60\n'])
	except KeyboardInterrupt:
		print("Closing OSCClient")
		osc.c.close()
		print("Done")















