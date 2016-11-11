#!/usr/bin/env python
#coding=utf-8

from string import Template

empty_selection = Template("")

pt_eta_selection = Template("\
        triggerMatched&&\
        isPtSelected &&\
        isEtaSelected\
        ")

id_oppcharge_selection = Template("\
        triggerMatched&&\
        isPtSelected &&\
        isIdentified &&\
        isOppositeCharge &&\
        isEtaSelected\
        ")

full_selection = Template("\
        triggerMatched&&\
        isPtSelected &&\
        isEtaSelected &&\
        isIdentified &&\
        isIsolated &&\
        isOppositeCharge\
        ")

full_selection_barrel_only = Template("\
        triggerMatched&&\
        isPtSelected &&\
        isEtaSelected &&\
        isIdentified &&\
        isIsolated &&\
        fabs(ele1Eta$flavour) < 1.5 && fabs(ele2Eta$flavour < 1.5) &&\
        isOppositeCharge\
        ")

only_isolation = Template("\
        isIsolated\
        ")

only_isolation_pt15 = Template("\
        isIsolated&&\
        ele1Pt$flavour > 15\
        ")

loose_isolation_pt15 = Template("\
        triggerMatched &&\
        ele1Iso$flavour / ele1Pt$flavour < 0.3 &&\
        ele1Pt$flavour > 15\
        ")

only_identification = Template("\
        isIdentified &&\
        ele1Pt$flavour > 15\
        ")

pt15ele1 = Template("\
        ele1Pt$flavour > 15\
        ")

full_no_charge = Template("\
        triggerMatched&&\
        isPtSelected &&\
        isEtaSelected &&\
        isIdentified &&\
        isIsolated\
        ")

only_pt = Template("\
        isPtSelected &&\
        isOppositeCharge\
        ")

pt15both = Template("\
        ele1Pt$flavour > 15 &&\
        ele2Pt$flavour > 15\
        ")
