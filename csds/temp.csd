<CsoundSynthesizer>
<CsOptions>
-odac1 -Ma -B256 -b64
</CsOptions>
<CsInstruments>
sr=44100
ksmps=1
nchnls=2
0dbfs=1

massign 0,10

ga_mix_1_0	init	0
ga_mix_1_1 	init	0
ga_mix_2_0	init	0
ga_mix_2_1 	init	0
ga_mix_3_0	init	0
ga_mix_3_1 	init	0
ga_mix_4_0	init	0
ga_mix_4_1 	init	0
ga_sub_Master_0 	init	0
ga_sub_Master_1	init	0

gk_HFdamp init 0.6266102195
gk_revLev init 0.4652525783
gk_roomSize init 0.5080189705
gk_chan1 init -6.1999998093
gk_auto4 init 0
gk_auto5 init 0
gk_masterVol init 0
gk_freq init 1000
gk_Q init 0.1
gk_env init .5

girecord init 0
girecordto init 11

gklevelL init 0.5
gklevelR init 0.5

gisine ftgen 0,0,2^12,10,1

	opcode blueEffect0,aa,aa
ain1,ain2	xin
arev1,arev2 freeverb ain1,ain2,gk_roomSize,gk_HFdamp,sr,1
aout1 = (arev1*gk_revLev)+(ain1*(1-gk_revLev))
aout2 = (arev2*gk_revLev)+(ain2*(1-gk_revLev))
xout 	aout1,aout2
	endop

alwayson 1     ; signal interface
alwayson 2      ; metronome
alwayson 20   ; mixer
alwayson 100
massign 1,10

instr 1  ; I/F
gk_chan1 chnget "chan1"
gk_chan2 chnget "chan2"
gk_chan3 chnget "chan3"
gk_chan4 chnget "chan4"

gk_masterVol chnget "Master"

gk_freq chnget "freq"
gk_Q chnget "Q"
gk_env chnget "env"
gk_pan chnget "pan1"
gk_revLev chnget "revLev"
gk_HFdamp chnget "HFdamp"
gk_roomSize chnget "roomSize"
;
gkrecord  chnget "record"
gkrecordto  chnget "recordto"
ktrig changed gkrecord, gkrecordto
 if ktrig == 1 then
     event     "i", 3, 0, .2, gkrecordto, gkrecord
 endif
endin

instr 2; triggering metronome
kTrig     metro     2; outputs "1" twice a second
 if kTrig == 1 then
          event     "i", 19, 0, 1 ;90, 42
 endif
endin

instr 3 ;    to set givariables via k vars..p4 = gkrecordto, p5 = gkrecord
    girecordto = p4
    girecord = p5
    print girecordto
    print girecord
endin

instr 10    ; midi recorder and trigger
;   p4=key, p5=vel


mididefault   60, p3
midinoteonkey p5, p4
inote	init p5
ivel	init p4

instrnum = girecordto + inote/100 + ivel/100000
event_i "i", instrnum, 0, -1, inote, ivel ;call with indefinite duration
kend release ;get a "1" if instrument is turned off
if kend == 1 then
event "i", -instrnum, 0, 1 ;then turn this instance off
endif

istrt times
krel release
if (krel == 0) kgoto nothing
kendt times
kdur =  kendt - istrt
;prints to file
if girecord==1 then
    Sscore    strcpy "scores/record1.sco"
    fprintks Sscore, "i %2.0f\\t%15.6f\\t%15.6f\\t%d\\t%d\\n", girecordto, istrt, kdur, inote, ivel
endif
turnoff

nothing:
endin

	instr 11	; VCO
ifreq	= cpsmidinn(p4)
iamp	 = p5/127

kenv	madsr	0.001, 0, .8, 0.2
avco vco iamp, ifreq, 1, 0.5, gisine
amoog moogvcf avco,kenv*gk_env*gk_freq, gk_Q
kpan2 = (1 - gk_pan)*3.14159265*.5
kpanl = sin(kpan2)
kpanr = cos(kpan2)
ga_mix_1_0 = ga_mix_1_0 +  kpanl*amoog
ga_mix_1_1 = ga_mix_1_1 +  kpanr*amoog
	endin


instr 19; metronome sound
reset:
timout 0, 1, impulse; jump to pulse generation section for 1 second
reinit reset; reninitialize pass from label 'reset'
impulse:
aenv expon 1, 0.3, 0.0001; a short percussive amplitude envelope
aSig poscil aenv*.6, 500, gisine
out aSig
rireturn
endin

	instr 20 	;Mixer Instrument
ktempdb = gk_chan1
ga_mix_1_0 = ga_mix_1_0 * ktempdb
ga_mix_1_1 = ga_mix_1_1 * ktempdb
ga_mix_1_0, ga_mix_1_1	blueEffect0	ga_mix_1_0, ga_mix_1_1
ga_sub_Master_0 	sum	ga_sub_Master_0, ga_mix_1_0
ga_sub_Master_1	    sum	ga_sub_Master_1, ga_mix_1_1

ktempdb = gk_chan2
ga_mix_2_0 = ga_mix_2_0 * ktempdb
ga_mix_2_1 = ga_mix_2_1 * ktempdb
ga_mix_2_0, ga_mix_2_1	blueEffect0	ga_mix_2_0, ga_mix_2_1
ga_sub_Master_0 	sum	ga_sub_Master_0, ga_mix_2_0
ga_sub_Master_1	    sum	ga_sub_Master_1, ga_mix_2_1

ktempdb = gk_masterVol
ga_sub_Master_0 = ga_sub_Master_0 * ktempdb
ga_sub_Master_1 = ga_sub_Master_1 * ktempdb
ksL rms ga_sub_Master_0
gklevelL = gklevelL + ksL
chnset gklevelL, "chanL"
ksR rms ga_sub_Master_1
gklevelR = gklevelR + ksR
chnset gklevelR, "chanR"
outc ga_sub_Master_0, ga_sub_Master_1
ga_mix_1_0 = 0
ga_mix_1_1 = 0
ga_sub_Master_0 = 0
ga_sub_Master_1 = 0

	endin

instr 100
gksL = gklevelL
gklevelL = 0
gksR = gklevelR
gklevelR = 0

endin
</CsInstruments>
<CsScore>
;#include "scores/recorded1.sco"
i 10 0  3600
</CsScore>
</CsoundSynthesizer>