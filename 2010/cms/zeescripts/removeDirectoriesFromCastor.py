#!/usr/bin/env python


import commands
import re
import os


def removeFiles(paths, sampleName, sampleWeight):
    	for path in paths:
            output = commands.getoutput("nsls "+path)
            outFiles = re.split(r'\n',output)
            for fname in outFiles:
			if re.search("pat_fromAOD_PF2PAT",fname)!=None:
                            rm = "rfrm "+path+fname
                            print rm
                            os.system(rm)

def createFiles(paths, sampleName, sampleWeight):
    newDir = "/castor/cern.ch/user/b/bianchi/CMSSW370p2/"
    newDir2 = "/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/"
    #os.system("rfmkdir "+newDir)
    #os.system("rfmkdir "+newDir2)
    mkdir = "rfmkdir "+newDir2+sampleName
    chmod = "rfchmod +775 "+newDir2+sampleName
    print mkdir,chmod
    os.system(mkdir)
    os.system(chmod)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/May6thPDSkim2_SD_EG_TauRel/",
	 "/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/SD_EG_TauRel"]
#createFiles(paths,"Data_ee",1)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Run2010AJul6thReReco"]
createFiles(paths,"Data",1)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Zee/"]
createFiles(paths,"Zee",1300.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Ztautau/"]
createFiles(paths,"Ztautau",1300.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/WJets-madgraph/"]
createFiles(paths,"WJets-madgraph",24170.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Wenu/"]
createFiles(paths,"Wenu",6153.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/TTbar/"]
createFiles(paths,"TTbar",149.8 )

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/QCDEM2030/"]
createFiles(paths,"QCDEM2030",0.2355*1000000000*0.0073)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/QCDEM3080/"]
createFiles(paths,"QCDEM3080",0.0593*1000000000*0.059)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/QCDEM80170/"]
createFiles(paths,"QCDEM80170",0.906*1000000*0.148)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/BctoE2030/"]
createFiles(paths,"BctoE2030",0.2355*1000000000*0.00046)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/BctoE3080/"]
createFiles(paths,"BctoE3080",0.0593*1000000000*0.00234)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/BctoE80170/"]
createFiles(paths,"BctoE80170",0.906*1000000*0.0104)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet015/"]
createFiles(paths,"PhotonJet015",8446*10000000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet1520/"]
createFiles(paths,"PhotonJet1520",1.147*100000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet2030/"]
createFiles(paths,"PhotonJet2030",5.718*10000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet3050/"]
createFiles(paths,"PhotonJet3050",1.652*10000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet5080/"]
createFiles(paths,"PhotonJet5080",2.723*1000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet80120/"]
createFiles(paths,"PhotonJet80120",4.462*100)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet120170/"]
createFiles(paths,"PhotonJet120170",8.443*10)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet170300/"]
createFiles(paths,"PhotonJet170300",2.255*10)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/PhotonJet300500/"]
createFiles(paths,"PhotonJet300500",1.545)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Comm10May27thSkim_SD_EG/"]
createFiles(paths,"DataComm10May",1.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Run2010AMay27thReReco/"]
createFiles(paths,"DataRunMay27",1.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Run2010APromptReco/"]
createFiles(paths,"DataRunPrompt",1.)
