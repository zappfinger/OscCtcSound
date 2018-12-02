<CsoundSynthesizer>
<CsOptions>
-odac1 -M0 -B256 -b64 --midi-key=4 --midi-velocity-amp=5
</CsOptions>
<CsInstruments>
sr=44100
ksmps=1
nchnls=2
0dbfs=1

ga_mix_1_0	init	0
ga_mix_1_1 	init	0
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

gklevelL init 0.5
gklevelR init 0.5

	opcode blueEffect0,aa,aa
ain1,ain2	xin
arev1,arev2 freeverb ain1,ain2,gk_roomSize,gk_HFdamp,sr,1
aout1 = (arev1*gk_revLev)+(ain1*(1-gk_revLev))
aout2 = (arev2*gk_revLev)+(ain2*(1-gk_revLev))
xout 	aout1,aout2
	endop

alwayson 1     ; signal interface
alwayson 20   ; mixer
alwayson 100
massign 1,11

instr 1  ; I/F
gk_masterVol chnget "Master"
gk_chan1 chnget "chan1"
gk_freq chnget "freq"
gk_Q chnget "Q"
gk_env chnget "env"
gk_pan chnget "pan1"
gk_revLev chnget "revLev"
gk_HFdamp chnget "HFdamp"
gk_roomSize chnget "roomSize"
endin

	instr 11	; VCO
ifreq	= cpsmidinn(p4)
iamp	 = p5/1

kenv	madsr	0.001, 0, .8, 0.2
isin ftgenonce 0, 0, 65536, 10, 1
avco vco iamp, ifreq, 1, 0.5, isin
amoog moogvcf avco,kenv*gk_env*gk_freq, gk_Q
kpan2 = (1 - gk_pan)*3.14159265*.5
kpanl = sin(kpan2)
kpanr = cos(kpan2)
ga_mix_1_0 = ga_mix_1_0 +  kpanl*amoog
ga_mix_1_1 = ga_mix_1_1 +  kpanr*amoog
	endin


	instr 20 	;Mixer Instrument
ktempdb = gk_chan1
ga_mix_1_0 = ga_mix_1_0 * ktempdb
ga_mix_1_1 = ga_mix_1_1 * ktempdb
ga_mix_1_0, ga_mix_1_1	blueEffect0	ga_mix_1_0, ga_mix_1_1
ga_sub_Master_0 	sum	ga_sub_Master_0, ga_mix_1_0
ga_sub_Master_1	sum	ga_sub_Master_1, ga_mix_1_1
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
e 3600
</CsScore>
</CsoundSynthesizer>