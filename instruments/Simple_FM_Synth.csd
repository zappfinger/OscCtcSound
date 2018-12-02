<CsoundSynthesizer>
<CsInstruments>

; Make sure CsOptions are not ignored in the preferences,
; Otherwise Realtime MIDI input will not work.

instr 3 ; Simple two operator FM synth

ifreq = p4  ; From p4 in the score or cps from MIDI note

kmodfactor chnget "modfactor"
kmodindex chnget "modindex"
; Mod envelope 
kmodatt chnget "modatt"
kmoddec chnget "moddec"
kmodsus chnget "modsus"
kmodrel chnget "modrel"
amodenv madsr i(kmodatt), i(kmoddec), i(kmodsus), i(kmodrel)

kmodfreq = kmodfactor*ifreq
; Index = Am * fc/fm
kmodamp = kmodindex*kmodfactor*ifreq
; Modulator 2
amod poscil amodenv*kmodamp, kmodfreq, 1

;Carrier amp envelope
kaatt chnget "aatt"
kadec chnget "adec"
kasus chnget "asus"
karel chnget "arel"
aenv madsr i(kaatt), i(kadec), i(kasus), i(karel)

; Carrier
aout poscil aenv, ifreq+amod, 1

; Output
klevel chnget "level"
;utvalue "index", kmodindex

outs aout*klevel, aout*klevel
endin

instr 98 ; Trigger instrument from button
kfreq chnget "freq"
event "i", 1, 0, p3, kfreq
turnoff
endin

instr 99 ;Always on instrument
; This instrument updates the modulator's frequencies
; which depend on the base frequency and the freq.
; factors.
kfreq chnget "freq"
kmodfactor chnget "modfactor"
;outvalue "mod1freq", kfreq*kmodfactor


;Turn on or off according to checkbox

kon chnget "on"
ktrig changed kon

if ktrig == 1 then
	if kon == 1 then
		event "i", 3, 0, -1, kfreq
	elseif kon == 0 then
		turnoff2 3, 0, 1
	endif
endif

endin

</CsInstruments>
<CsScore>
f 1 0 4096 10 1
i 99 0 3600
</CsScore>
</CsoundSynthesizer>
