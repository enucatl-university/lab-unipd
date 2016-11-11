include(/usr/bin/circuit.macros/libcct.m4)
.PS                            # Pic input begins with .PS
cct_init                       # Set defaults

elen = 1                   # Variables are allowed; default units are inches
Origin: Here                   # Position names are capitalized
  Sorg: source(up_ elen*3/4, v); llabel(-,V_0,+)
  [linewid=0.7*linewid; resistor(up_ elen*3/4)];  llabel(,R_G,)
  line right_ elen
  dot
  {                           # Save current position and direction
     source(down_ elen*3/2,"V")
     dot
     }                        # Restore position and direction
  source(right_ elen,"A")
  resistor(down_ elen*3/2); variable()
  line to Origin
.PE                            # Pic input ends
