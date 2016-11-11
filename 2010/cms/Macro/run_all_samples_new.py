#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

import sys
import os
import subprocess

from pflow_analysis_template_cfg import *

#########################################
def processSingleSample(path, sampleName):
    cmssw = "CMSSW370p2"
    process.source.fileNames = cms.untracked.vstring()
    if sampleName == "Data":
    	cmssw = "CMSSW361p2"
    	process.configurationMetadata.preselectionEff = -1
    	process.PatTriggerAnalyzer.triggerResultsLabel = cms.InputTag("TriggerResults", "", "HLT")
        print("sample is Data {0}".format(sampleName))
    else:
        process.PatTriggerAnalyzer.triggerResultsLabel = cms.InputTag("TriggerResults", "", "REDIGI37X")
    command = "nsls {0} | tail -n 500".format(path)
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = output.communicate()[0]
    outFiles = output.split('\n')
    for fname in outFiles:
        if "root" in fname:
            process.source.fileNames.append("rfio:" + os.path.join(path, fname))
    process.TFileService = cms.Service("TFileService", 
            fileName = cms.string("PFAnalysis_NEW_{0}.root".format(sampleName)),
            closeFileFast = cms.untracked.bool(True)
            )

    process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(-1)
    )
    with open('tmpConfig_{0}.py'.format(sampleName),'w') as out:
        out.write(process.dumpPython())

    try:
        command = "cmsBatch.py 100 -o Batch_SD_{0}  ./tmpConfig_{0}.py -r /castor/cern.ch/user/a/abis/fullsim_background/PFAnalysis_NEW_{0}.root".format(sampleName, cmssw)
        print(command)
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print("Execution failed", e, file=sys.stderr)

    try:
        command = "rm -f tmpConfig_{0}.py*".format(sampleName)
        print(command)
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print("Execution failed", e, file=sys.stderr)

#########################################    

#paths = ["/castor/cern.ch/user/b/bianchi/CMSSW361p2/patLayer/Run2010AJul6thReReco/"]
#processSingleSample(paths,"Data",1)

#Signal Zee:

#folders = [
#"BCtoE_20_30",
#"BCtoE_30_80",
#"BCtoE_80_170",
#"QCDEM_20_30",
#"QCDEM_30_80",
#"QCDEM_80_170",
#]

#castor_home = "/castor/cern.ch/user/a/abis"
#base_folder = "fastsim_background"


folders = [
"BctoE2030",
"BctoE3080",
"BctoE80170",
"QCDEM2030",
"QCDEM80170",
"Wenu",
"TTbar",
"PhotonJet015",
"PhotonJet120170",
"PhotonJet1520",
"PhotonJet170300",
"PhotonJet2030",
"PhotonJet300500",
"PhotonJet3050",
"PhotonJet5080",
"PhotonJet80120",
]

castor_home = "/castor/cern.ch/user/b/bianchi"
base_folder = "/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer"

folders = dict([(folder, os.path.join(castor_home, base_folder, folder)) for folder in folders])

for name, folder in folders.iteritems():
    processSingleSample(folder, name)

#florian_folder = "/castor/cern.ch/user/b/beaudett/grid/CMSSW370p2/QCD_EMEnriched_Pt30to80"
#processSingleSample(florian_folder, "QCDEM3080")
