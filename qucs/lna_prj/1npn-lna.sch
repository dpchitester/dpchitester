<Qucs Schematic 0.0.19>
<Properties>
  <View=192,-195,1821,1243,0.751916,0,0>
  <Grid=10,10,1>
  <DataSet=1npn-lna.dat>
  <DataDisplay=1npn-lna.dpl>
  <OpenDisplay=0>
  <Script=1npn-lna.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <C C2 5 460 310 -26 17 0 0 "1 uF" 1 "" 0 "neutral" 0>
  <C C1 5 680 410 10 17 0 1 "1 uF" 1 "" 0 "neutral" 0>
  <C C3 5 860 270 24 -13 0 1 "1 uF" 1 "" 0 "neutral" 0>
  <_BJT Q1 1 570 170 -41 -26 1 2 "npn" 0 "8.11e-14" 0 "1" 0 "1" 0 "0.5" 0 "0.225" 0 "113" 0 "24" 0 "1.06e-11" 0 "2" 0 "0" 0 "2" 0 "205" 0 "4" 0 "0" 0 "0" 0 "0.137" 0 "0.343" 0 "1.37" 0 "2.95e-11" 0 "0.75" 0 "0.33" 0 "1.52e-11" 0 "0.75" 0 "0.33" 0 "1" 0 "0" 0 "0.75" 0 "0" 0 "0.5" 0 "3.97e-10" 0 "0" 0 "0" 0 "0" 0 "8.5e-08" 0 "26.85" 0 "0" 0 "1" 0 "1" 0 "0" 0 "1" 0 "1" 0 "0" 0 "1.5" 0 "3" 0 "1.11" 0 "26.85" 0 "1" 0>
  <GND * 1 620 470 0 0 0 0>
  <GND * 1 490 120 0 0 0 0>
  <GND * 1 800 -130 0 0 0 2>
  <Vdc VCC 1 800 -100 47 -55 0 3 "4.7" 1>
  <GND * 1 860 350 0 0 0 0>
  <GND * 1 680 470 0 0 0 0>
  <GND * 1 340 80 0 0 0 0>
  <GND * 1 330 420 0 0 0 0>
  <.DC DC1 5 1000 -140 0 56 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SP SP1 1 1000 -40 0 93 0 0 "lin" 1 "1 MHz" 1 "30 MHz" 1 "30" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <R R2 5 800 280 -30 99 0 1 "70k" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R R1 5 800 100 23 -11 0 1 "70k" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <Pac P2 1 340 50 18 -26 0 1 "2" 1 "50" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Tr Tr2 1 540 20 -29 38 1 2 "7" 1>
  <Tr Tr3 1 650 270 38 -29 0 1 "1" 1>
  <GND * 1 800 350 0 0 0 0>
  <.Opt Opt1 1 1290 -110 0 53 0 0 "Sim=SP1" 0 "DE=3|50|2|20|0.85|1|3|1e-6|10|100" 0 "Var=Zin|yes|3.868368E+001|0|50|LIN_DOUBLE" 0 "Goal=OG|MIN|1" 0>
  <Pac P1 1 330 390 18 -26 0 1 "1" 1 "Zin" 1 "-40 dbM" 0 "1 GHz" 0 "26.85" 0>
  <Eqn Eqn3 5 1050 260 -47 20 0 0 "Gain=20*log10(abs(S[2,1])^2)" 1 "VSWR=rtoswr(S[1,1])" 1 "OG=avg(abs(VSWR),1e6:30e6)" 1 "yes" 0>
  <R R3 5 620 410 -83 -1 0 1 "112" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <Eqn OptValues1 1 1360 60 -28 15 0 0 "Zin=3.868368E+001" 1 "yes" 0>
</Components>
<Wires>
  <490 310 570 310 "" 0 0 0 "">
  <620 350 620 380 "" 0 0 0 "">
  <680 350 680 380 "" 0 0 0 "">
  <620 350 680 350 "" 0 0 0 "">
  <800 210 860 210 "" 0 0 0 "">
  <860 210 860 240 "" 0 0 0 "">
  <570 200 570 310 "" 0 0 0 "">
  <600 170 680 170 "" 0 0 0 "">
  <680 170 680 240 "" 0 0 0 "">
  <680 300 680 350 "" 0 0 0 "">
  <620 300 620 310 "" 0 0 0 "">
  <570 310 620 310 "Ve" 550 330 7 "">
  <620 210 800 210 "" 0 0 0 "">
  <620 210 620 240 "" 0 0 0 "">
  <620 440 620 470 "" 0 0 0 "">
  <570 50 570 140 "" 0 0 0 "">
  <490 50 510 50 "" 0 0 0 "">
  <490 50 490 120 "" 0 0 0 "">
  <570 -10 800 -10 "" 0 0 0 "">
  <800 -70 800 -10 "" 0 0 0 "">
  <800 -10 800 70 "" 0 0 0 "">
  <800 130 800 210 "" 0 0 0 "">
  <800 210 800 250 "" 0 0 0 "">
  <860 300 860 350 "" 0 0 0 "">
  <680 440 680 470 "" 0 0 0 "">
  <340 -10 340 20 "" 0 0 0 "">
  <340 -10 510 -10 "" 0 0 0 "">
  <330 310 430 310 "" 0 0 0 "">
  <330 310 330 360 "" 0 0 0 "">
  <800 310 800 350 "" 0 0 0 "">
  <430 310 430 310 "Vin" 370 250 0 "">
  <680 170 680 170 "Vb" 690 140 0 "">
</Wires>
<Diagrams>
  <Tab 320 1050 748 93 3 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 1 315 0 225 "" "" "">
	<"OG" #0000ff 0 3 1 0 0>
	<"Tr3" #0000ff 0 3 1 0 0>
	<"Vb.V" #0000ff 0 3 1 0 0>
	<"VCC.I" #0000ff 0 3 1 0 0>
	<"Ve.V" #0000ff 0 3 1 0 0>
	<"Vin.V" #0000ff 0 3 1 0 0>
	<"Zin" #0000ff 0 3 1 0 0>
  </Tab>
  <Rect 320 860 1009 309 3 #c0c0c0 1 00 1 1e+06 2e+06 3e+07 1 0.906391 0.01 0.95 1 -1 0.5 1 315 0 225 "" "" "">
	<"Gain" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
