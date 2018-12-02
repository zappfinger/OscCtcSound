<CsoundSynthesizer>
<CsOptions>
-odac1 -M0
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 128
;0dbfs = 1
nchnls = 2

instr 2
kwaveform = 0
kwave = p6
kwavetrig	changed	kwave


if kwavetrig = 1 then
	reinit REINIT_VCO
endif

REINIT_VCO:
kkey init p4					;initialize key number
kvel init p5					;initialize velocity
midinoteonkey kkey, kvel
printk2 kkey
avco vco kvel/127, cpsmidinn(kkey), i(kwave),0.5,1
outs avco*kvel, avco*kvel
endin

</CsInstruments>
<CsScore>
f 0 30
; Table #1, a sine wave.
f 1 0 65536 10 1

e 3600
</CsScore>
</CsoundSynthesizer>
