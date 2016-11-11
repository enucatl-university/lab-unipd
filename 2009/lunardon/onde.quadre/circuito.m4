include(/usr/bin/circuit.macros/libcct.m4)
.PS                            # Pic input begins with .PS
cct_init                       # Set defaults

l = 1                    # Variables are allowed; default units are inches
Origin: Here                   # Position names are capitalized
  source(up_ l, U)
  line right_ l*3/4
  dot
  {                           # Save current position and direction
     capacitor(down_ l); rlabel(,C_p,)
     dot
     }                        # Restore position and direction
  resistor(right_ l); llabel(,R=\unit[55.6]{k\ohm},)
  dot
  {                           # Save current position and direction
     capacitor(down_ l); rlabel(,C,)
     dot
     }                        # Restore position and direction
  line right_ l
  dot
  {                           # Save current position and direction
     resistor(down_ l); rlabel(,R_o,)
     dot
     }                        # Restore position and direction
  line right_ l*2/4
  ebox(down_ l,l/2,0.3*l)
  ground(,,,D)
  line to Origin
.PE                            # Pic input ends
