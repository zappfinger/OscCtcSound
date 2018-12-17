'''
    ctcsoundSession.py:
    
    Copyright (C) 2016 Francois Pinot
    
    This code is free software; you can redistribute it
    and/or modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.
    
    Csound is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public
    License along with Csound; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
    02111-1307 USA
'''

import os
import ctypes
import ctcsound
import time

class CsoundSession(ctcsound.Csound):
    """A class for running a csound session"""
    
    def __init__(self, csdFileName=None):
        """Start a csound session, eventually loading a csd file"""
        ctcsound.Csound.__init__(self)
        self.pt = None
        #if csdFileName and os.path.exists(csdFileName):
        if csdFileName:
            self.csd = csdFileName
            self.startThread()
        else:
            self.csd = None
    
    def startThread(self):
        if self.compile_("csoundSession", self.csd) == 0 :
            self.createMessageBuffer(0)
            self.pt = ctcsound.CsoundPerformanceThread(self.cs)
            self.pt.play()
            
    def resetSession(self, csdFileName=None):
        """Reset the current session, eventually loading a new csd file"""
        if csdFileName and os.path.exists(csdFileName):
            self.csd = csdFileName
        if self.csd:
            self.stopPerformance()
            self.startThread()
    
    def stopPerformance(self):
        """Stop the current score performance if any"""
        if self.pt:
            if self.pt.status() == 0:
                self.pt.stop()
            self.pt.join()
            self.pt = None
        self.cleanup()

    def csdFileName(self):
        """Return the loaded csd filename or None"""
        return self.csd
        
    def note(self, pfields, absp2mode = 0):
        """Send a score note to a csound instrument"""
        return self.pt.scoreEvent(absp2mode, 'i', pfields)
        
    def scoreEvent(self, eventType, pfields, absp2mode = False):
        """Send a score event to csound"""
        self.pt.scoreEvent(absp2mode, eventType, pfields)
    
    def flushMessagesold(self):
        """Wait until all pending messages are actually received by the performance thread"""
        if self.pt:
            self.pt.flushMessageQueue()

    def flushMessages(self, cs, delay=0):
        s = ""
        if delay > 0:
            time.sleep(delay)
        for i in range(cs.messageCnt()):
            s += cs.firstMessage()
            cs.popFirstMessage()
        return s

    def printMessages(self, cs, delay=0):
        s = self.flushMessages(cs, delay)
        if len(s) > 0: print(s)

if __name__ == '__main__':
    cs = CsoundSession("/Users/richard/PycharmProjects/OscCtcSound/csds/Mono_Synth.csd")
    time.sleep(1)
    #cs.stopPerformance()
    #cs.reset()
    #cs.resetSession("/Users/richard/PycharmProjects/OscCtcSound/csds/vco2test.csd")
    cs.compileCsd("/Users/richard/PycharmProjects/OscCtcSound/instruments/FM2nd.csd")
    #cs.reset()
    #cs.start()
    while 1:
        time.sleep(1)



