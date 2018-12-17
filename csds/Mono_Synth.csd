<CsoundSynthesizer>
<CsOptions>
-odac1 -Ma -B256 -b64
</CsOptions>
<CsInstruments>

; A monophonic legato instrument, playable from a MIDI keyboard.
; By Jim Aikin, based on a method suggested by Victor Lazzarini.

sr = 44100
ksmps = 4
nchnls = 2
0dbfs = 1

alwayson	"ToneGenerator"
giSaw	ftgen	0, 0, 8192, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1

gkCheck init 0
gkPitch init 260

instr 1		; activated from MIDI channel 1, tracks the pitch
gkPitch	cpsmidib	2
gkCheck = 1
endin

instr ToneGenerator

kon	active 1		; check whether any instances of instr 1 are active

; velocity sensing -- only accept a new velocity input if
; there's no note overlap (if kon == 1) -- scale the velocity
; to a range of 0.2 - 1.0
kvel init 0
kstatus, kchan, kdata1, kdata2 midiin
if kstatus == 144 && kdata2 != 0 && kon == 1 then
	kvel = kdata2 * 0.006 + 0.2
	event "i", 3, 0, -1, 880
endif

katt chnget "att"
krel chnget "rel"
; amplitude control
kampraw init 0
if kon != 0 then
	kampraw = 0.5 * kvel
	kenvramp = katt		; 50 = fast attack
else
	kampraw = 0
	kenvramp = krel	; 1 = slow release
endif
kamp	tonek	kampraw, kenvramp

kpitchglide chnget "pitchglide"
ipitchglide = 4			; higher numbers cause faster glide
kpitch	tonek	gkPitch, kpitchglide

; oscillators
idetune = 0.3
asig1	oscil	kamp, kpitch + idetune, giSaw
asig2	oscil	kamp, kpitch, giSaw
asig3	oscil	kamp, kpitch - idetune, giSaw
asig = asig1 + asig2 + asig3

; if no MIDI keys are pressed, reinit the filter envelope
if gkCheck == 1 && kon == 0 then
	reinit filtenv
endif

ifiltdec1 = 1.5
ifiltdec2 = 3
filtenv:
kfilt	expseg	500, 0.01, 8000, ifiltdec1, 2000, ifiltdec2, 500, 1, 500
rireturn

; smooth the filter envelope so a reinit won't cause it to jump --
; also have the cutoff track the keyboard and velocity
kfilt	tonek	(kfilt * (0.6 + kvel * 0.5)) + kpitch, kenvramp

afilt	lpf18	asig, kfilt, 0.3, 0.1

		outs	afilt, afilt
endin

</CsInstruments>
<CsScore>

e 3600

</CsScore>
</CsoundSynthesizer>
