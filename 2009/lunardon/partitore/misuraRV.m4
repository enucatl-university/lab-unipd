include(/usr/bin/circuit.macros/libcct.m4)
.PS                            # Pic input begins with .PS
cct_init                       # Set defaults

elen = 0.75                    # Variables are allowed; default units are inches
Origin: Here                   # Position names are capitalized
  source(up_ elen*1.5, v); llabel(-,V_0,+)
  source(right_ elen*1.5,"A")
  dot
  {                           # Save current position and direction
     source(down_ elen*3/4,"V")
     [linewid = linewid*2/3; resistor(down_ elen*3/4)]; rlabel(,R_V,)
     dot
     }                        # Restore position and direction
  line right_ elen
  resistor(down_ elen*1.5); llabel(,R_C,)
  line to Origin
.PE                            # Pic input ends
