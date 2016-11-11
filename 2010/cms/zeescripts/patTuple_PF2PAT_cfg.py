from PhysicsTools.PatAlgos.patTemplate_cfg import *

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source.fileNames = cms.untracked.vstring()

#for i in range(1, 2):
    #myFile = '/store/relval/CMSSW_3_6_0/RelValZEE/GEN-SIM-RECO/MC_36Y_V4-v1/0013/6ABDA7F9-AC49-DF11-9E89-0018F3D09708.root'
    #print myFile
    #process.source.fileNames.append(myFile)
       
process.source.fileNames = cms.untracked.vstring('rfio:/castor/cern.ch/user/j/jwerner/merge_prompt_1.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_prompt_2.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_june14.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_july16_1.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_july16_2.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_july16_3.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_july16_4.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_july16_5.root',
                                                 'rfio:/castor/cern.ch/user/j/jwerner/merge_july16_6.root',
                                                 )

# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.pfTools import *

postfix = "PFlow"
runOnMC = False

from PFAnalyses.CommonTools.diCandidateProducer_cfi import diTauProducer
process.recoDiEle = diTauProducer.clone()
process.recoDiEle.srcLeg1 = 'patElectronsTriggerMatchEmbedder'
process.recoDiEle.srcLeg2 = 'patElectronsTriggerMatchEmbedder'
process.recoDiEle.recoMode = ''
process.recoDiEle.dRmin12 = 0.3
process.recoDiEle.useLeadingTausOnly = False

process.recoDiElePFlow = diTauProducer.clone()
process.recoDiElePFlow.srcLeg1 = 'patElectronsTriggerMatchEmbedderPFlow'
process.recoDiElePFlow.srcLeg2 = 'patElectronsTriggerMatchEmbedderPFlow'
process.recoDiElePFlow.recoMode = ''
process.recoDiElePFlow.dRmin12 = 0.3
process.recoDiElePFlow.useLeadingTausOnly = False

# trigger matching
process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
process.patTrigger.processName = 'HLT'

process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerMatcher_cfi")
process.electronTriggerMatchHLTEle15LWL1R.src = "selectedPatElectrons"
#process.electronTriggerMatchHLTEle15LWL1R.pathNames = cms.vstring()
process.electronTriggerMatchHLTEle15LWL1R.pathNames.append( 'HLT_Photon15_Cleaned_L1R' )
process.electronTriggerMatchHLTEle15LWL1R.pathNames.append( 'HLT_Photon10_L1R' )
process.electronTriggerMatchHLTEle15LWL1R.pathNames.append( 'HLT_Ele10_LW_L1R' )
process.electronTriggerMatchHLTEle15LWL1R.maxDeltaR = 0.5
process.electronTriggerMatchHLTEle15LWL1R.maxDPtRel = 0.5
process.patTriggerMatcher += process.electronTriggerMatchHLTEle15LWL1R
process.patTriggerMatcher.remove( process.patTriggerMatcherElectron )
process.patTriggerMatcher.remove( process.patTriggerMatcherMuon )
process.patTriggerMatcher.remove( process.patTriggerMatcherTau )
#process.patTriggerEvent.patTriggerMatches  = [ "electronTriggerMatchHLTEle15LWL1R" ]
#process.patTriggerEvent.processName = 'HLT'

############################
process.patElectronsTriggerMatchEmbedder = cms.EDProducer("PATTriggerMatchElectronEmbedder",
                                                  src = cms.InputTag( "selectedPatElectrons" ),
                                                  matches = cms.VInputTag( "electronTriggerMatchHLTEle15LWL1R" )
                                                  )

process.patTriggerSequence += process.patElectronsTriggerMatchEmbedder
############################

from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger, switchOnTriggerMatchEmbedding, switchOnTriggerStandAlone
#switchOnTrigger( process )
switchOnTriggerStandAlone( process )


usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= runOnMC, postfix=postfix) 


if not runOnMC:
    removeMCMatching(process,["All"])

getattr(process,"electronTriggerMatchHLTEle15LWL1R"+postfix).src = "selectedPatElectronsPFlow"
#getattr(process,"patTriggerEvent"+postfix).patTriggerMatches  = ["electronTriggerMatchHLTEle15LWL1RPFlow" ]

getattr(process,"patElectronsTriggerMatchEmbedder"+postfix).src = "selectedPatElectronsPFlow"
getattr(process,"patElectronsTriggerMatchEmbedder"+postfix).matches  = ["electronTriggerMatchHLTEle15LWL1RPFlow" ]

# PF electron isolation
getattr(process,"isoDepElectronWithCharged"+postfix).ExtractorPSet.Diff_r = 9999.0
getattr(process,"isoDepElectronWithCharged"+postfix).ExtractorPSet.Diff_z = 9999.0

getattr(process,"isoValElectronWithCharged"+postfix).deposits[0].deltaR = 0.4
getattr(process,"isoValElectronWithNeutral"+postfix).deposits[0].deltaR = 0.4
getattr(process,"isoValElectronWithNeutral"+postfix).deposits[0].weight = '0.33333'
getattr(process,"isoValElectronWithPhotons"+postfix).deposits[0].deltaR = 0.4

getattr(process,"pfIsolatedElectrons"+postfix).isolationValueMaps = cms.VInputTag(
    cms.InputTag("isoValElectronWithCharged"+postfix),
    cms.InputTag("isoValElectronWithPhotons"+postfix)
    )

# remove isolation criteria

process.pfIsolatedElectrons.isolationCuts = cms.vdouble(99999.,99999.)
process.pfIsolatedElectrons.combinedIsolationCut = cms.double(9999)
getattr(process,"pfIsolatedElectrons"+postfix).isolationCuts = cms.vdouble(99999.,99999.)
getattr(process,"pfIsolatedElectrons"+postfix).combinedIsolationCut = cms.double(9999)

# build objects w/o top projections
getattr(process,"pfAllElectrons"+postfix).src = 'pfNoPileUp'+postfix # no overlap with muons by def?
getattr(process,"pfNoElectron"+postfix).bottomCollection = 'pfNoPileUp'+postfix
#getattr(process,"allPfJets"+postfix).src = 'pfNoPileUp'+postfix # jets used for tau id



# this is for filtering on HLT path
process.hltHighLevelElectron = cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults::HLT"),
     HLTPaths = cms.vstring('HLT_Ele10_LW_L1R', 'HLT_Ele15_LW_L1R','HLT_Photon15_Cleaned_L1R','HLT_Photon10_L1R'),  
     eventSetupPathsKey = cms.string(''),                 
     andOr = cms.bool(True), #True (OR) accept if ANY is true, False (AND) accept if ALL are true
     throw = cms.bool(True)                               
 )

process.scrapping = cms.EDFilter("FilterOutScraping",
                                applyfilter = cms.untracked.bool(True),
                                debugOn = cms.untracked.bool(False),
                                numtrack = cms.untracked.uint32(10),
                                thresh = cms.untracked.double(0.25)
                                )

##########################################################################
process.diEleCountFilter = cms.EDFilter("PATCandViewCountFilter",
                                        minNumber = cms.uint32(2),
                                        maxNumber = cms.uint32(999999),
                                        src = cms.InputTag('selectedPatElectrons'),
                                        )

process.diEleCountFilterPFlow = process.diEleCountFilter.clone()
process.diEleCountFilterPFlow.src = cms.InputTag('selectedPatElectronsPFlow')

process.p1 = cms.Path(
    process.scrapping +
    process.patDefaultSequence*
    process.recoDiEle*
    process.diEleCountFilter
    )

process.p2 = cms.Path(
    process.scrapping +
    getattr(process,"patPF2PATSequence"+postfix)*
    process.recoDiElePFlow*
    process.diEleCountFilterPFlow
    )

process.diEleFilter = cms.EDFilter("HLTHighLevel",
                                   TriggerResultsTag = cms.InputTag('TriggerResults','',process.name_()),
                                   HLTPaths = cms.vstring('p1','p2'),
                                   eventSetupPathsKey = cms.string(''), 
                                   andOr = cms.bool(True),   
                                   throw = cms.bool(True),
                                   filter = cms.bool(False)
                                   )
##########################################################################


#process.patDefaultSequence.remove( process.makePatJets )
#process.patDefaultSequence.remove( process.selectedPatJets )
#process.patDefaultSequence.remove( process.cleanPatJets )
#process.patDefaultSequence.remove( process.countPatJets )


# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning

process.out.outputCommands = cms.untracked.vstring('drop *',
                                                   *patEventContentNoCleaning ) 
process.out.outputCommands.extend( cms.vstring('keep *_recoDiEle_*_*',
                                               'keep *_recoDiElePFlow_*_*',
                                               'drop *_selectedPatMuons_*_*',
                                               'drop *_selectedPatMuonsPFlow_*_*',
                                               'drop *_selectedPatPFParticles_*_*',
                                               'drop *_selectedPatPhotons_*_*',
                                               'drop *_selectedPatTaus_*_*',
                                               'drop *_selectedPatTausPFlow_*_*',
                                               'keep *_offlineBeamSpot_*_*',
                                               'keep *_offlinePrimaryVertices*_*_*',
                                               'keep edmTriggerResults_TriggerResults*_*_*',
                                               'keep *_hltTriggerSummaryAOD_*_*',
                                               'keep *_patElectronsTriggerMatchEmbedder*_*_*'
                                               )
                                   )

process.out.fileName = cms.untracked.string('analysis_DiEle_PF2PAT.root')

process.out.SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('p1','p2')
    )

#process.end = cms.EndPath(process.out + process.diEleFilter)

process.MessageLogger.cerr.FwkReport.reportEvery = 100
