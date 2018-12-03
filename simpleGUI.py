import PySimpleGUI as sg
from csoundSession import CsoundSession
from DBclass import *

def getLayout():
	layout = [[sg.Text(
		'      Master        chan1              freq              Q              env            pan1         revLev       ' \
		'HFdamp      roomSize            ')],
			  [sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=55),
			   sg.Slider(range=(0, 100), orientation='v', size=(10, 20), default_value=66),
			   sg.Slider(range=(20, 10000), orientation='v', size=(10, 20), default_value=7700),
			   sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=22),
			   sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=22),
			   sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=22),
			   sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=55),
			   sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=22),
			   sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=50),
			   sg.Graph(canvas_size=(40, 160), graph_bottom_left=(0, 0), graph_top_right=(80, 100),
						  background_color='red', key='graph')],
			  [sg.Button("Chord")],
			  [sg.Exit()]]
	return layout

db=db()
templ = db.select("select template, description, GUI from templates where name='VCO, mixer, effects';")
# get the GUI layout locally
layout = getLayout()
# or from database...
#exec(templ[0]['GUI'])

for t in templ:
	print(t['template'])
	text_file = open("csds/temp.csd", "w")
	text_file.write(t['template'])
	text_file.close()
window = sg.Window('Template: ' + t['description']).Layout(layout).Finalize()
graph = window.FindElement('graph')
#rectangle = graph.DrawRectangle((10,00), (40,40), fill_color='purple' )
#line = graph.DrawLine((0,0), (40,80), color='black')
cs = CsoundSession("/Users/richard/PycharmProjects/OscCtcSound/csds/temp.csd")
i=0
while True:
	event, values = window.Read(timeout=20)
	#print(event)
	if event == 'Chord':
		cs.scoreEvent('i', (11, 0, 1, 62, .80))
		cs.scoreEvent('i', (11, 0, 1, 66, .80))
		cs.scoreEvent('i', (11, 0, 1, 70, .80))
	cs.setControlChannel('Master', float(values[0])/100.)
	cs.setControlChannel('chan1', float(values[1])/100.)
	cs.setControlChannel('freq', float(values[2]))
	cs.setControlChannel('Q', float(values[3])/100.,)
	cs.setControlChannel('env', float(values[4])/100.)
	cs.setControlChannel('pan1', float(values[5])/100.)
	cs.setControlChannel('revLev', float(values[6])/100.)
	cs.setControlChannel('HFdamp', float(values[7])/100.)
	cs.setControlChannel('roomSize', float(values[8])/100.)
	chanL=cs.controlChannel('chanL')
	chanR=cs.controlChannel('chanR')
	graph.DrawRectangle((0, 00), (80, 200), fill_color='black')
	graph.DrawRectangle((0, 00), (40, int(chanL[0]*1600)), fill_color='green')
	graph.DrawRectangle((40, 00), (80, int(chanR[0]*1600)), fill_color='green')
	if event is None or event == 'Exit':
		break
	time.sleep(.1)

window.Close()