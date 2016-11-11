.PS                            # Pic input begins with .PS
cct_init                       # Set defaults

elen = 0.6                    # Variables are allowed; default units are inches
Origin: Here                   # Position names are capitalized
    up_
    T: bi_tr(up elen) with .E at Here
    Rc: resistor(up_ elen from T.C); rlabel(,R_c,)
    dot(at Rc.end); clabel(,,V_{cc})
    line left_ 0.75*elen from T.B
    {
        line up elen/2
        resistor(up_ elen); rlabel(,R_1,)
        dot; clabel(,,V_{cc})
    }
    {
        line down elen/2
        resistor(down_ 1.5*elen); llabel(,R_2,)
        ground(,T)
    }
    capacitor(left elen); llabel(,C_1,)
    dot; rlabel(,V_\text{in},)
    Re1: resistor(down 0.75*elen from T.E); clabel(R_{e1},,)
    Re2: resistor(down 0.75*elen); clabel(R_{e2},,)
    ground(,T)
    line right elen/2 from Re1.end
    capacitor(down 0.75*elen); llabel(,,C_2)
    ground(,T)
# 
    #add emitter follower
#
    line right elen from T.C
    TF:  bi_tr(up, elen) with .B at Here
    dot(at TF.E); clabel(,,V_{\text{out}})
    Re3: resistor(down elen from TF.E); clabel(,,R_{e3})
    ground(,T)
    line up elen/2 from TF.C
    dot; llabel(,V_{cc},)
.PE                            # Pic input ends
