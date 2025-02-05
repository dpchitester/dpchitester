<Qucs Schematic 0.0.22>
<Properties>
  <View=203,-178,709,210,2.1933,0,0>
  <Grid=10,10,1>
  <DataSet=aa-network.dat>
  <DataDisplay=aa-network.dpl>
  <OpenDisplay=1>
  <Script=aa-network.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
  <.PortSym -30 0 1 0>
  <Line -20 -10 40 0 #000080 2 1>
  <Line 20 -10 0 20 #000080 2 1>
  <Line -20 -10 0 20 #000080 2 1>
  <Line -30 0 10 0 #000080 2 1>
  <Line 20 0 10 0 #000080 2 1>
  <.PortSym 30 0 2 180>
  <Line -20 10 40 0 #000080 2 1>
  <.ID -50 44 MAGANT "1=R1=10=Rrad=" "1=C1=0==" "1=L1=0==">
</Symbol>
<Components>
  <Port P2 5 310 130 -67 13 0 0 "2" 1 "analog" 0 "v" 0 "" 0>
  <R R1 5 330 80 -82 -16 0 1 "R1" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <L L1 5 330 -10 -76 -16 0 1 "L1v" 1 "" 0>
  <C C1 5 390 -10 21 -15 0 1 "C1v" 1 "" 0 "neutral" 0>
  <Port P1 5 310 -130 -67 17 0 0 "1" 1 "analog" 0 "v" 0 "" 0>
  <Eqn Eqn1 5 560 -70 -47 20 0 0 "L1v=L1*1e-6" 1 "C1v=C1*1e-12" 1 "yes" 0>
</Components>
<Wires>
  <330 -130 330 -40 "" 0 0 0 "">
  <330 -130 390 -130 "" 0 0 0 "">
  <390 -130 390 -40 "" 0 0 0 "">
  <330 130 390 130 "" 0 0 0 "">
  <390 20 390 130 "" 0 0 0 "">
  <310 130 330 130 "" 0 0 0 "">
  <310 -130 330 -130 "" 0 0 0 "">
  <330 20 330 50 "" 0 0 0 "">
  <330 110 330 130 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
