# OSCsound - Version 0.3
# Author: Steven Yi
#
# Script for rapid live Csound application development with OSC
# 
# Licensed under LGPL. Please view LICENSE for more information.
#
#   modified by zappfinger to use ctcsound

from Oscy import *
from csoundSession import CsoundSession
from time import sleep
import argparse
import types

csd_file=''
cs = CsoundSession("/Users/richard/PycharmProjects/OscCtcSound/csds/vco2test.csd")

def csound_start(csd_file):
    global csound
    global csPerfThread

    csound = Csound()
    csound.SetOption("-odac")
    csound.Compile(csd_file)
    csound.Start()
    csPerfThread = CsoundPerformanceThread(csound)
    csPerfThread.Play()

def csound_stop():
    global csPerfThread
    global csound
    csPerfThread.Stop()
    csPerfThread.Join()
    csound.Stop()

###

server = None
run = True

def handle_timeout(self):
    self.timed_out = True

def handle_score(path, tags, args, source):
    global csPerfThread
    #print "TESTING", args[0]
    csPerfThread.InputMessage(args[0])

def handle_inst(path, tags, args, source):
    global csPerfThread
    #print "TESTING", args[0]
    #csound_stop()
    #csound_start(csd_file)
    sleep(2)
    csound.CompileOrc(args[0])

def handle_cc(path, tags, args, source):
    global csound
    print path
    if(len(args) != 2):
        print "Error: CC must have two args: channelName floatValue"
        return
    print "TESTING: %s %s"%(args[0], args[1])
    csound.SetChannel(args[0], args[1])

def default_callback(path, tags, args, source):
    global csound
    if path.startswith("/cc/"):
        csound.SetChannel(path[4:], args[0])
    else:
        print "ignoring message :", path, tags, args

def quit_callback(path, tags, args, source):
    global run
    run = False
    print "Quitting Server..."


def each_frame():
    global server
    server.timed_out = False
    while not server.timed_out:
        server.handle_request()


def server_start(port=7110):
    global server
    server = OSCServer ( ("localhost", port))
    server.timeout = 0

    server.handle_timeout = types.MethodType(handle_timeout, server)

    server.addMsgHandler("/sco", handle_score)
    server.addMsgHandler("/inst", handle_inst)
    server.addMsgHandler("/cc", handle_cc)
    server.addMsgHandler("/quit", quit_callback)
    server.addMsgHandler("default", default_callback)

def server_stop():
    global server
    server.close()



def main():
    global csd_file
    csd_file = './temp.csd'
    server_start(7710)
    csound_start(csd_file)
    while run:
        sleep(1)
        each_frame()

    csound_stop()
    server_stop()

if __name__ == '__main__':
    main()
