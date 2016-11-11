include(/usr/bin/circuit.macros/libcct.m4)
.PS                            # Pic input begins with .PS
cct_init                       # Set defaults

elen = 0.75                    # Variables are allowed; default units are inches
Origin: Here                   # Position names are capitalized
  source(up_ elen, v); llabel(-,V_0,+)
  [linewid = linewid*2/3; resistor(up_ elen)];  llabel(,R_G,)
  line right_ elen*1.5; b_current(I_1)
  dot; llabel(,A,)
  {                           # Save current position and direction
     resistor(down_ elen); rlabel(,R_5,); b_current(I_2)
     resistor(down_ elen); rlabel(,R_6,)
     dot; clabel(,,B)
     }                        # Restore position and direction
  line right_ elen*1.5;  b_current(I_3)
  resistor(down_ elen/2); llabel(,R_1,)
  resistor(down_ elen/2); llabel(,R_2,)
  resistor(down_ elen/2); llabel(,R_3,)
  resistor(down_ elen/2); llabel(,R_4,)
  line to Origin
.PE                            # Pic input ends
