#!/usr/bin/env python


import commands
import re
import os

castor = "/castor/cern.ch/user/b/bianchi/CMSSW356/patLayer/MC/"

output = commands.getoutput("nsls "+castor)

outFiles = re.split(r'\n',output)

for name in outFiles:
    isEmpty = commands.getstatusoutput("edmFileUtil -f rfio:"+castor+name)
    outputSplit = re.split(r'\W',isEmpty[1])
    if outputSplit[30] != '0':
        print "File "+name+" has "+outputSplit[30]+" events"
        cp = "rfcp "+castor+name+" ./MC"
        print cp
        os.system(cp)

