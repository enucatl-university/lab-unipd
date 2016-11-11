.PS                            # Pic input begins with .PS
cct_init                       # Set defaults

elen = 0.6                    # Variables are allowed; default units are inches
Origin: Here                   # Position names are capitalized
    dot; llabel(V_{\text{in}},,)
    diode(right_ elen)
    {
        resistor(down_ elen); rlabel(,R,)
        ground(,T)
    }
    line right_ elen*.5;
    dot; llabel(,,V_{\text{out}})
.PE                            # Pic input ends
