import FWCore.ParameterSet.Config as cms

process = cms.Process("ZEE")

from PFAnalyses.CommonTools.Selectors.electronIsoSelectorPSet_cff import electronIsoSelectorPSet
from PFAnalyses.CommonTools.Selectors.electronSelectorPSet_cff import electronSelectorPSet


# Optimized iso+ID selection:
#   P(1) = 0.976316 P(2) = 0.942105 P(1,2) = 0.919298 P(2|1) = 0.941599
# optimizing at 95% on the subleading electron => (0.25,0.2) BL, (0.24,0) EC
#   P(1) = 0.946491 P(2) = 0.883772 P(2,1) = 0.839912 P(2|1) = 0.887396
# optimizing at 95% on the leading electron => (0.14,0.25) BL, (0.17,0.10) EC 

EleIsoSelector1 = electronIsoSelectorPSet.clone()

isolationCuts = cms.VPSet(
    cms.PSet(
      name=cms.string("combined95BarrelLeg1"),
      absoluteCut=cms.double(3.4),
      relativeCut=cms.double(0.14),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(1)
      ),
    cms.PSet(
      name=cms.string("combined95EndCapLeg1"),
      absoluteCut=cms.double(3.6),
      relativeCut=cms.double(0.17),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(1)
      ),
    cms.PSet(
      name=cms.string("combined95BarrelLeg2"),
      absoluteCut=cms.double(3.4),
      relativeCut=cms.double(0.25),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(1)
      ),
    cms.PSet(
      name=cms.string("combined95EndCapLeg2"),
      absoluteCut=cms.double(3.6),
      relativeCut=cms.double(0.24),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(1)
      ),
    cms.PSet(
      name=cms.string("combined95EndCap"),
      absoluteCut=cms.double(3.6),
      relativeCut=cms.double(0.17),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(1)
      ),
    cms.PSet(
      name=cms.string("combined95Barrel"),
      absoluteCut=cms.double(3.4),
      relativeCut=cms.double(0.14),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(1)
      ),
    cms.PSet(
      name=cms.string("combined"),
      absoluteCut=cms.double(3.0),
      relativeCut=cms.double(0.15),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(1)
      ),
    cms.PSet(
      name=cms.string("charged"),
      absoluteCut=cms.double(9999),
      relativeCut=cms.double(9999),
      chargedWeight=cms.double(1),
      photonWeight=cms.double(0),
      neutralWeight=cms.double(0)
    ),
    cms.PSet(
      name=cms.string("gamma"),
      absoluteCut=cms.double(9999),
      relativeCut=cms.double(9999),
      chargedWeight=cms.double(0),
      photonWeight=cms.double(1),
      neutralWeight=cms.double(0)
    ),
    cms.PSet(
      name=cms.string("neutral"),
      absoluteCut=cms.double(9999),
      relativeCut=cms.double(9999),
      chargedWeight=cms.double(0),
      photonWeight=cms.double(0),
      neutralWeight=cms.double(1)
    )
)

EleIsoSelector1.isolationCuts = isolationCuts

EleIsoSelector1.chargedIsoPar = cms.PSet(
    coneSize=cms.double(0.3),
    vetoes=cms.VPSet(
        cms.PSet(
           type = cms.string("ThresholdVeto"),
           threshold = cms.double(0.0) 
        ),
        cms.PSet(
           type = cms.string("ConeVeto"),
           deltaR = cms.double(0.0)  
        ),
        cms.PSet(
           type = cms.string("RectangularEtaPhiVeto"),
           dEta = cms.double(0.0), 
           dPhi = cms.double(0.0)
        )
    )
)

EleIsoSelector1.neutralIsoPar = cms.PSet(
    coneSize=cms.double(0.3),
    vetoes=cms.VPSet(
        cms.PSet(
           type = cms.string("ConeVeto"),
           deltaR = cms.double(0.00)  
        ),
    )
)

EleIsoSelector1.photonsIsoPar = cms.PSet(
    coneSize=cms.double(0.3),
    vetoes=cms.VPSet(
        cms.PSet(
           type = cms.string("RectangularEtaPhiVeto"),
           dEta = cms.double(0.0), 
           dPhi = cms.double(0.0)
        )
    )
)

EleIsoSelector2 = EleIsoSelector1.clone()

######################################################################
EleIsoSelector1_03 = EleIsoSelector1.clone()

EleIsoSelector1_04 = EleIsoSelector1.clone()
EleIsoSelector1_04.chargedIsoPar.coneSize = 0.4
EleIsoSelector1_04.neutralIsoPar.coneSize = 0.4
EleIsoSelector1_04.photonsIsoPar.coneSize = 0.4

EleIsoSelector2_03 = EleIsoSelector2.clone()
EleIsoSelector2_04 = EleIsoSelector2.clone()
EleIsoSelector2_04.chargedIsoPar.coneSize = 0.4
EleIsoSelector2_04.neutralIsoPar.coneSize = 0.4
EleIsoSelector2_04.photonsIsoPar.coneSize = 0.4

#######################################################################

EleSelectorBL = electronSelectorPSet.clone()
EleSelectorEC = electronSelectorPSet.clone()
EleSelectorBL95Leg1 = electronSelectorPSet.clone()
EleSelectorEC95Leg1 = electronSelectorPSet.clone()
EleSelectorBL95Leg2 = electronSelectorPSet.clone()
EleSelectorEC95Leg2 = electronSelectorPSet.clone()

EleSelectorBL.mvaCut = 0.25
EleSelectorBL.maxMissingHitCut = 2
EleSelectorEC.mvaCut = 0.10
EleSelectorEC.maxMissingHitCut = 2

EleSelectorBL95Leg1.mvaCut = 0.25
EleSelectorBL95Leg1.maxMissingHitCut = 2
EleSelectorEC95Leg1.mvaCut = 0.10
EleSelectorEC95Leg1.maxMissingHitCut = 2

EleSelectorBL95Leg2.mvaCut = 0.20
EleSelectorBL95Leg2.maxMissingHitCut = 2
EleSelectorEC95Leg2.mvaCut = 0.0
EleSelectorEC95Leg2.maxMissingHitCut = 2


#######################################################################


#######################################################################

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

extName = 'tmp'
weight=1.0

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    #'file:/tmp/bianchi/analysis_DiEle_PF2PAT_11_1_HLZ.root'
    #'rfio:/castor/cern.ch/user/b/bianchi/CMSSW370p2/patLayer/Zee/analysis_DiEle_PF2PAT_10_1_Rih.root'
    #"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_20_1_GDQ.root"
    #"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_234_1_1D8.root"
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_10_1_aco.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_11_1_Vzh.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_12_1_Q3G.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_134_1_utP.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_13_1_W6j.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_14_1_0CW.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_15_1_eMU.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_169_1_1uf.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_16_1_yao.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_173_1_2yu.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_174_1_mAy.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_17_1_PDN.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_18_1_uz3.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_198_1_M4j.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_19_1_CV2.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_1_1_q5B.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_1_2_WLm.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_20_1_GDQ.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_220_1_uNS.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_234_1_1D8.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_249_1_a7d.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_2_1_3ci.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_2_1_srs.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_2_2_8tt.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_3_1_dPQ.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_49_1_CYD.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_4_1_bH0.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_51_1_11P.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_58_1_6xc.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_5_1_Htn.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_6_1_p6Q.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_7_1_0dn.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_8_1_gpa.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_93_1_leO.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_9_1_uUy.root",
"rfio:/castor/cern.ch/user/a/abis/ntuple/patTuple_9_3_iua.root",
    )
                            
                            )


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('1.0'),
    name = cms.untracked.string( extName ),
    annotation = cms.untracked.string('None'),
    preselectionEff = cms.untracked.double(-1) #1.0 ==> automatic scaling
    )

selFlavours = cms.untracked.vstring("PF_SYM","PF_ASYM","EG")

process.PatTriggerAnalyzer = cms.PSet(
    evtWeight=cms.double(weight),
    #triggerResultsLabel = cms.InputTag("TriggerResults","","REDIGI37X"),
    triggerResultsLabel = cms.InputTag("TriggerResults","","HLT"),
    triggerItemName = cms.string("HLT_Ele15_LW_L1R"),
    #triggerItemName = cms.string("HLT_Photon15_Cleaned_L1R"),
    selectionFlavours = selFlavours
    )

process.Summary =  cms.PSet(
    selectionFlavours = selFlavours
    )


process.FWLiteZeeAnalyzer = cms.PSet(

    selectionFlavours = selFlavours,
    
    zBosLabelPF = cms.untracked.InputTag("recoDiElePFlow"),
    zBosLabelEG = cms.untracked.InputTag("recoDiEle"),
    offlinePrimaryVertecesLabel =  cms.InputTag("offlinePrimaryVerticesWithBS"),
    evtWeight = cms.double(weight),

    verbose=cms.bool(False),
    useVertex = cms.bool(False),
    HLTpathNames = cms.vstring("none",
                               "HLT_Photon15_Cleaned_L1R",
                               "HLT_Photon10_L1R",
                               "HLT_Ele15_LW_L1R"
                               ),

    hOverEMaxBL = cms.untracked.double(0.05),
    deltaPhiMaxBL = cms.untracked.double(0.8),
    deltaEtaMaxBL = cms.untracked.double(0.007),
    sigmaIIMaxBL = cms.untracked.double(0.01),
    hOverEMaxEC = cms.untracked.double(0.07),
    deltaPhiMaxEC = cms.untracked.double(0.7),
    deltaEtaMaxEC = cms.untracked.double(999.), #0.01
    sigmaIIMaxEC = cms.untracked.double(0.03),
    combIsoBL = cms.untracked.double(0.15),
    combIsoEC = cms.untracked.double(0.1),
    maxMissHitsBL = cms.untracked.double(2),
    maxMissHitsEC = cms.untracked.double(2),

    elePhaseSpaceSelector1 = cms.PSet(
    pt = cms.VPSet(
    cms.PSet( min = cms.double(20.), max = cms.double(9999.) ),
    ),
    eta = cms.VPSet(
    cms.PSet( min = cms.double(-1.4442), max = cms.double(1.4442) ),
    cms.PSet( min = cms.double( 1.566), max = cms.double(2.5) ),
    cms.PSet( min = cms.double(-2.5), max = cms.double(-1.566) ),
    ),
    phi = cms.VPSet(
    cms.PSet( min = cms.double(-10), max = cms.double(10) ) 
    ),
    verbose = cms.untracked.bool( False )
    ),

    elePhaseSpaceSelector2 = cms.PSet(
    pt = cms.VPSet(
    cms.PSet( min = cms.double(20.), max = cms.double(9999.) ),
    ),
    eta = cms.VPSet(
    cms.PSet( min = cms.double(-1.4442), max = cms.double(1.4442 ) ),
    cms.PSet( min = cms.double( 1.566), max = cms.double(2.5 ) ),
    cms.PSet( min = cms.double(-2.5), max = cms.double(-1.566) ),
    ),
    phi = cms.VPSet(
    cms.PSet( min = cms.double(-10), max = cms.double(10) ) 
    ),
    verbose = cms.untracked.bool( False )
    ),
    
    eleIsoSelector1 = EleIsoSelector1_04,
    eleIsoSelector2 = EleIsoSelector2_04,

    eleSelectorBLLeg1 = EleSelectorBL95Leg1,
    eleSelectorECLeg1 = EleSelectorEC95Leg1,
    eleSelectorBLLeg2 = EleSelectorBL95Leg2,
    eleSelectorECLeg2 = EleSelectorEC95Leg2,

    eleSelectorBL = EleSelectorBL,
    eleSelectorEC = EleSelectorEC
    
    
    )

from PFAnalyses.CommonTools.patJetAnalyzerPSet_cff import patJetAnalyzerPSet
myJetAnalyzer = patJetAnalyzerPSet.clone()
process.PatJetAnalyzer =myJetAnalyzer

process.ZeeEDFilterAnalyzer = cms.EDFilter("ZeeEDFilterAnalyzer",
                                           cfgFileName = cms.untracked.string("zElEl_ANA_data_cfg.py")
                                           )

process.p = cms.Path(
    process.ZeeEDFilterAnalyzer
    )

