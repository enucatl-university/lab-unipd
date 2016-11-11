.PS                            # Pic input begins with .PS
cct_init                       # Set defaults

elen = 0.6                    # Variables are allowed; default units are inches
Origin: Here                   # Position names are capitalized
    up_
    T: bi_tr with .E at Here
    ground(at T.E)
    RC: resistor(up_ elen from T.C); rlabel(,R_c,)
    dot(at T.C); rlabel(,V_c,)
    dot(at RC.end); clabel(,,V_0)
    RB: resistor(left_ elen from T.B); llabel(,R_b,)
    dot(at T.B); rlabel(,V_b,)
    dot(at RB.end); clabel(,,V_a)
.PE                            # Pic input ends
