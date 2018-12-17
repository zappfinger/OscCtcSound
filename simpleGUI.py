#import PySimpleGUIQt as sg
import PySimpleGUI as sg
from csoundSession import CsoundSession
from DBclass import *

MyButton = lambda text: sg.Button(text, size=(6,1), font='Helvetica 12', button_color=('white', 'blue'), key=text)
sButton = lambda text: sg.Button(text, size=(1,1), font='Helvetica 12', button_color=('white', 'blue'), key=text)
Slider = lambda range, default_value: sg.Slider(range=range, orientation='v', size=(8, 20), default_value=default_value,
	background_color='lightgreen')
chantype = sg.InputCombo(('midi','audio'), size=(10, 2))
rec = MyButton('Record')
recordto = [sg.Spin([i for i in range(1,5)], initial_value=1,enable_events=True,key='recchan'), sg.Text('Record channel')]
recording = False; cs=None
win1=None; win2=None; win3=None; win4=None
win1_active=False; win2_active=False; win3_active=False; win4_active=False

def getLayout():
	column1 = [[sg.Text('Channel 1', background_color='lightgreen', justification='center', size=(8, 1)), chantype],
				[sg.InputCombo(('VCO'), size=(20, 5), key='inst1',enable_events=True),sButton('M1'),sButton('S1')],
				[sg.Slider(range=(1, 100), key='chan1', orientation='h', size=(15, 20), default_value=85, \
						enable_events=True), MyButton('Detail1')]]

	column2 = [[sg.Text('Channel 2', background_color='#d3dfda', justification='center', size=(8, 1)), chantype],
				[sg.InputCombo((instlist), size=(20, 5), key='inst2',enable_events=True),sButton('M2'),sButton('S2')],
				[sg.Slider(range=(1, 100), key='chan2', orientation='h', size=(15, 20), default_value=85, \
						enable_events=True), MyButton('Detail2')]]

	column3 = [[sg.Text('Channel 3', background_color='#d3dfda', justification='center', size=(8, 1)), chantype],
				[sg.InputCombo((instlist), size=(20, 5), key='inst3'),sButton('M3'),sButton('S3')],
				[sg.Slider(range=(1, 100), key='chan3', orientation='h', size=(15, 20), default_value=85, \
						enable_events=True), MyButton('Detail3')]]

	column4 = [[sg.Text('Channel 4', background_color='#d3dfda', justification='center', size=(8, 1)), chantype],
				[sg.InputCombo((instlist), size=(20, 5), key='inst4'),sButton('M4'),sButton('S4')],
				[sg.Slider(range=(1, 100), key='chan4', orientation='h', size=(15, 20), default_value=85, \
						enable_events=True), MyButton('Detail4')]]

	track1 = [sg.Column(column1, background_color='lightgreen'),
		sg.Graph(canvas_size=(900, 100), graph_bottom_left=(0, 0), graph_top_right=(900, 100),
			background_color='grey', key='graphch1')]

	track2 = [sg.Column(column2, background_color='#d3dfda'),
		sg.Graph(canvas_size=(900, 100), graph_bottom_left=(0, 0), graph_top_right=(900, 100),
			background_color='grey', key='graphch2')]

	track3 = [sg.Column(column3, background_color='#d3dfda'),
		sg.Graph(canvas_size=(900, 100), graph_bottom_left=(0, 0), graph_top_right=(900, 100),
			background_color='grey', key='graphch3')]

	track4 = [sg.Column(column4, background_color='#d3dfda'),
		sg.Graph(canvas_size=(900, 100), graph_bottom_left=(0, 0), graph_top_right=(900, 100),
			background_color='grey', key='graphch4')]

	transcol = [[sg.Text('', size=(20, 2), font=('Helvetica', 20), justification='center', key='secs')],
		[MyButton('Record'), MyButton('Play'), MyButton('Stop'), MyButton('Reset')],
		[sg.Checkbox('Metronome', key='metro', default=True)],
		recordto]

	op=[[sg.Output(size=(80,15), background_color='black', text_color='yellow')]]
	#op = [[sg.Output(size=(80, 10))]]

	layout = [track1,track2,track3,track4,
		[sg.Text('_' * 210)],
		[sg.Text('     revLev        HFdamp     roomSize   Master')],
		[sg.Slider(range=(1, 100), orientation='v', size=(8, 20), key='revLev', default_value=22),
		sg.Slider(range=(1, 100), orientation='v', size=(8, 20), key='HFdamp',default_value=55),
		sg.Slider(range=(1, 100), orientation='v', size=(8, 20), key='roomSize',default_value=22),
		sg.Slider(range=(1, 100), orientation='v', size=(8, 20), key='Master',default_value=50),
		sg.Graph(canvas_size=(40, 160), graph_bottom_left=(0, 0), graph_top_right=(80, 100), background_color='red', key='graph'),
		sg.VerticalSeparator(pad=None), sg.Column(transcol), sg.VerticalSeparator(pad=None), sg.Column(op)]]

	return layout

def openDetail(gui, procgui, proc=1):
	exec(gui)
	if proc:processDetail(procgui)

def processDetail(procgui):
	exec(procgui)

def openDetail1(proc=0):
	global win1
	layout2 = [[sg.Column([[sg.Text('           freq              Q              env             pan')],
		[Slider((20, 10000), 7700),
		Slider((0, 100), 55),
		Slider((1, 100), 22),
		Slider((1, 100), 22)],
		[sg.Button('Exit'), sg.Button("Chord")]], background_color='lightgreen')]]
	win1 = sg.Window('VCO detail').Layout(layout2)
	if proc:processDetail1()
	return win1

def processDetail1():
	global win1_active
	ev2, vals2 = win1.Read(timeout=100)
	# print(vals2)
	if ev2 == 'Chord':
		cs.scoreEvent('i', eval("(11, 0, 1, 62, 80)"))
		cs.scoreEvent('i', (11, 0, 1, 66, 80))
		cs.scoreEvent('i', (11, 0, 1, 70, 80))
	if vals2 is not None:
		cs.setControlChannel('freq', float(vals2[0]))
		cs.setControlChannel('Q', float(vals2[1]) / 100.)
		cs.setControlChannel('env', float(vals2[2]) / 100.)
		cs.setControlChannel('pan1', float(vals2[3]) / 100.)
	if ev2 is None or ev2 == 'Exit':
		win1_active = False
		win1.Close()

def openDetail2():
	global win2
	layout2 = [[sg.Column([[sg.Text('         pre           post          shape1         shape2       wave')],
		[Slider((0, 200), 50),
		Slider((0, 200), 55),
		Slider((0, 200), 22),
		Slider((0, 200), 22),
		Slider((0, 200), 200)],
		[sg.Button('Exit'), sg.Button("Chord")]], background_color='lightgreen')]]
	win2 = sg.Window('FM bass 1 detail').Layout(layout2)
	return win2

def processDetail2():
	global win2_active
	ev2, vals2 = win2.Read(timeout=100)
	# print(vals
	if ev2 == 'Chord':
		cs.scoreEvent('i', eval("(12, 0, 1, 62, 80)"))
		cs.scoreEvent('i', (12, 0, 1, 66, 80))
		cs.scoreEvent('i', (12, 0, 1, 70, 80))
	if vals2 is not None:
		cs.setControlChannel('fmb1_pre', float(vals2[0]))
		cs.setControlChannel('fmb1_post', float(vals2[1]) / 100.)
		cs.setControlChannel('fmb1_shap1', float(vals2[2]) / 100.)
		cs.setControlChannel('fmb1_shap2', float(vals2[3]) / 100.)
		cs.setControlChannel('fmb1_wave', float(vals2[4]) / 100.)
	if ev2 is None or ev2 == 'Exit':
		win2_active = False
		win2.Close()

db=db()
templ = db.select("select template, description, GUI from templates where name='VCO, mixer, effects';")
ins = db.select("select name from instruments")
instlist=[]
for inst in ins:
	instlist.append(inst['name'])
# get the GUI layout locally
layout = getLayout()
# or from database...
#exec(templ[0]['GUI'])

started=False

for t in templ:
	pass
	#print(t['template'])
#	text_file = open("csds/temp.csd", "w")
#	text_file.write(t['template'])
#	text_file.close()
window = sg.Window('Template: ' + t['description']).Layout(layout).Finalize()
graph = window.FindElement('graph')
graph.DrawRectangle((0, 00), (80, 200), fill_color='black')
#line = graph.DrawLine((0,0), (40,80), color='black')
#cs = CsoundSession("/Users/richard/PycharmProjects/OscCtcSound/csds/temp.csd")
i=0
offs=4

cs = CsoundSession("/Users/richard/PycharmProjects/OscCtcSound/csds/temp.csd")
cs.start()
started = True
d1 = openDetail1(1)  # trick to get default values to instrument
d1.Close()
d2 = openDetail2()
d2.Close()

def loadScore():
	global cs
	with open("/Users/richard/PycharmProjects/OscCtcSound/scores/recorded1.sco") as f:
		lines = f.read().splitlines()
	for lin in lines:
		l = lin.split()
		sl = ','.join(l[1:])
		es = "(%s)" % sl
		cs.scoreEvent('i', eval(es))

while True:
	event, values = window.Read(timeout=20)
	if event is not None:
		if event.startswith('inst'):
			chan=int(event.split('inst')[1])+10
			instrgui = db.select("select instr, gui, procgui from instruments where name='%s'" % values[event])
			cs.compileOrc(instrgui[0]['instr'] % chan)
			gui = instrgui[0]['gui']
			print(gui)
			procgui = instrgui[0]['procgui']
			openDetail(gui, procgui); win2_active = True
		elif event=='recchan':
			recto = int(window.FindElement('recchan').Get())
			cs.setControlChannel('recordto', recto + 10)		# channel 1 is actually instrument 11, etc

	if win2_active:processDetail(procgui)


	#
	if started:
		if values is not None:
			cs.setControlChannel('chan1', float(values['chan1'])/100.)
			cs.setControlChannel('chan2', float(values['chan2'])/100.)
			cs.setControlChannel('chan3', float(values['chan3'])/100.)
			cs.setControlChannel('chan4', float(values['chan4'])/100.)

			cs.setControlChannel('revLev', float(values['revLev'])/100.)
			cs.setControlChannel('HFdamp', float(values['HFdamp'])/100.)
			cs.setControlChannel('roomSize', float(values['roomSize'])/100.)
			cs.setControlChannel('Master', float(values['Master'])/100.)

			chanL=cs.controlChannel('chanL')
			chanR=cs.controlChannel('chanR')
			t = int(cs.scoreTime())
			window.FindElement('secs').Update('{:02d}:{:02d}.{:02d}'.format((t // 100) // 60, (t // 100) % 60, t % 60))
			try:
				graph.DrawRectangle((0, 00), (80, 200), fill_color='black')
				graph.DrawRectangle((0, 00), (40, int(chanL[0]*1000)), fill_color='green')
				graph.DrawRectangle((40, 00), (80, int(chanR[0]*1000)), fill_color='green')
			except:
				pass

	if event=='Stop':
		cs.stopPerformance()
		started=False
	if event=='Record' and started==False:
		#cs = CsoundSession("/Users/richard/PycharmProjects/OscCtcSound/csds/temp.csd")
		cs.start()
		started = True
		recording = True
	elif event=='Record':
		started = True
		recording = True
	if recording:
		# get instrument where we are recording to
		recto = int(window.FindElement('recchan').Get())
		cs.setControlChannel('record', 1)
		cs.setControlChannel('recordto', recto + 10)		# channel 1 is actually instrument 11, etc

	if event=='Play' and not recording:
		loadScore()
		cs.start()
		started=True
	if event=='Reset': cs.reset()
	if event is None or event == 'Exit':
		break

	#while (cs.performKsmps() == 0):
	cs.printMessages(cs, .0001)
	time.sleep(.15)

window.Close()