#!/usr/bin/env python

import os
import re
import commands

from zElEl_ANA_mc_cfg import *

#########################################
def processSingleSample(paths, sampleName, sampleWeight):
	cmssw = "CMSSW370p2"
	if re.search("Data",sampleName)!=None:
		cmssw = "CMSSW361p2"
	process.source.fileNames = cms.untracked.vstring()
	for path in paths:
		output = commands.getoutput("nsls "+path)
		outFiles = re.split(r'\n',output)
		for fname in outFiles:
			if re.search("analysis",fname)!=None:
				process.source.fileNames.append('rfio:'+path+fname)
	process.configurationMetadata.name=sampleName
	if re.search("Data",sampleName)!=None:
		process.configurationMetadata.preselectionEff= -1
		process.PatTriggerAnalyzer.triggerResultsLabel = cms.InputTag("TriggerResults","","HLT")
	out = open('tmpConfig_'+sampleName+'.py','w')
	out.write(process.dumpPython())
	out.close()

	command = "cmsBatch.py 100 -o Batch_SD_"+sampleName+" -q 1nh ./tmpConfig_"+sampleName+".py -r /castor/cern.ch/user/b/bianchi/"+cmssw+"/rootAll/PFAnalysis_"+sampleName+".root -p analyzeElectrons"
	print command
	os.system(command)
	os.system("rm -f tmpConfig_"+sampleName+".py*")
#########################################	

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Run2010AJul6thReReco/"]
processSingleSample(paths,"Data",1)

##Signal Zee:

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/Zee/"]
processSingleSample(paths,"Zee",1300.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/Ztautau/"]
processSingleSample(paths,"Ztautau",1300.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/WJets-madgraph/"]
processSingleSample(paths,"WJets-madgraph",24170.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/Wenu/"]
processSingleSample(paths,"Wenu",6153.)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/TTbar/"]
processSingleSample(paths,"TTbar",149.8 )

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/QCDEM2030/"]
processSingleSample(paths,"QCDEM2030",0.2355*1000000000*0.0073)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/QCDEM3080/"]
#processSingleSample(paths,"QCDEM3080",0.0593*1000000000*0.059)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/QCDEM80170/"]
processSingleSample(paths,"QCDEM80170",0.906*1000000*0.148)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/BctoE2030/"]
processSingleSample(paths,"BctoE2030",0.2355*1000000000*0.00046)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/BctoE3080/"]
processSingleSample(paths,"BctoE3080",0.0593*1000000000*0.00234)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/BctoE80170/"]
processSingleSample(paths,"BctoE80170",0.906*1000000*0.0104)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet015/"]
processSingleSample(paths,"PhotonJet015",8446*10000000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet1520/"]
processSingleSample(paths,"PhotonJet1520",1.147*100000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet2030/"]
processSingleSample(paths,"PhotonJet2030",5.718*10000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet3050/"]
processSingleSample(paths,"PhotonJet3050",1.652*10000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet5080/"]
processSingleSample(paths,"PhotonJet5080",2.723*1000)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet80120/"]
processSingleSample(paths,"PhotonJet80120",4.462*100)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet120170/"]
processSingleSample(paths,"PhotonJet120170",8.443*10)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet170300/"]
processSingleSample(paths,"PhotonJet170300",2.255*10)

paths = ["/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/PhotonJet300500/"]
processSingleSample(paths,"PhotonJet300500",1.545)

