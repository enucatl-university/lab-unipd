# Auto generated configuration file
# using: 
# Revision: 1.172.2.5 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: bJpsiX_7TeV.cfi -s GEN:ProductionFilterSequence,FASTSIM -n 10 --conditions auto:startup --pileup=NoPileUp --geometry DB
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.RandomServiceInitialization_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator7TeV_cfi')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('FastSimulation.Configuration.HLT_8E29_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.CommonInputs_cff')
process.load('FastSimulation.Configuration.EventContent_cff')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.172.2.5 $'),
    annotation = cms.untracked.string('bJpsiX_7TeV.cfi nevts:10'),
    name = cms.untracked.string('PyReleaseValidation')
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)
# Input source
process.source = cms.Source("EmptySource")

# Output definition
process.output = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    fileName = cms.untracked.string('bJpsiX_7TeV_cfi_GEN_FASTSIM.root'),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('skim_step')
    )
)

# Additional output definition

# Other statements
process.famosPileUp.PileUpSimulator = process.PileUpSimulatorBlock.PileUpSimulator
process.famosPileUp.PileUpSimulator.averageNumber = 0
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)

# set correct vertex smearing
process.Realistic7TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic7TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic7TeVCollisionVtxSmearingParameters
# Apply ECAL/HCAL miscalibration
process.ecalRecHit.doMiscalib = True
process.hbhereco.doMiscalib = True
process.horeco.doMiscalib = True
process.hfreco.doMiscalib = True
# Apply Tracker and Muon misalignment
process.famosSimHits.ApplyAlignment = True
process.misalignedTrackerGeometry.applyAlignment = True

process.misalignedDTGeometry.applyAlignment = True
process.misalignedCSCGeometry.applyAlignment = True

process.GlobalTag.globaltag = 'START36_V10::All'

process.FilterEle = cms.EDFilter("FilterElectrons",
                                 egElectronCollection = cms.InputTag("gsfElectrons"),
                                 pfElectronCollection = cms.InputTag("particleFlow"),
                                 egElePtMin = cms.double(20.),
                                 pfElePtMin = cms.double(15.),
                                 egEleNMin = cms.double(1),
                                 pfEleNMin = cms.double(1),
                                 verbose = cms.bool(False)
                                 )

process.doubleEMenrichingfilter = cms.EDFilter("doubleEMEnrichingFilter",
					       filterAlgoPSet = cms.PSet(
	requireTrackMatch = cms.bool(False),
	caloIsoMax = cms.double(3.0),
	isoGenParConeSize = cms.double(0.1),
	seedThreshold = cms.double(1.5),
	eTThreshold = cms.double(2.0),
	tkIsoMax = cms.double(3.0),
	hOverEMax = cms.double(0.5),
	isoGenParETMin = cms.double(2.0),
	genParSource = cms.InputTag("genParticlesForFilter"),
	isoConeSize = cms.double(0.2),
	clusterThreshold = cms.double(2.0)
	)
					       )

process.generator = cms.EDFilter("Pythia6GeneratorFilter",
				 pythiaPylistVerbosity = cms.untracked.int32(1),
				 filterEfficiency = cms.untracked.double(0.0227),
				 pythiaHepMCVerbosity = cms.untracked.bool(False),
				 comEnergy = cms.double(7000.0),
				 crossSection = cms.untracked.double(20800000000.0),
				 maxEventsToPrint = cms.untracked.int32(0),
				 PythiaParameters = cms.PSet(
	pythiaUESettings = cms.vstring('MSTJ(11)=3     ! Choice of the fragmentation function',
				       'MSTJ(22)=2     ! Decay those unstable particles',
				       'PARJ(71)=10.   ! for which ctau  10 mm',
				       'MSTP(2)=1      ! which order running alphaS',
				       'MSTP(33)=0     ! no K factors in hard cross sections',
				       'MSTP(51)=10042     ! CTEQ6L1 structure function chosen',
				       'MSTP(52)=2     ! work with LHAPDF',
				       'MSTP(81)=1     ! multiple parton interactions 1 is Pythia default',
				       'MSTP(82)=4     ! Defines the multi-parton model',
				       'MSTU(21)=1     ! Check on possible errors during program execution',
				       'PARP(82)=1.8387   ! pt cutoff for multiparton interactions',
				       'PARP(89)=1960. ! sqrts for which PARP82 is set',
				       'PARP(83)=0.5   ! Multiple interactions: matter distrbn parameter',
				       'PARP(84)=0.4   ! Multiple interactions: matter distribution parameter',
				       'PARP(90)=0.16  ! Multiple interactions: rescaling power',
				       'PARP(67)=2.5    ! amount of initial-state radiation',
				       'PARP(85)=1.0  ! gluon prod. mechanism in MI',
				       'PARP(86)=1.0  ! gluon prod. mechanism in MI',
				       'PARP(62)=1.25   ! ',
				       'PARP(64)=0.2    ! ',
				       'MSTP(91)=1     !',
				       'PARP(91)=2.1   ! kt distribution',
				       'PARP(93)=15.0  ! '),
	processParameters = cms.vstring('MSEL=1                ! QCD high pT processes',
					'CKIN(3)=6.            ! minimum pt hat for hard interactions',
					'CKIN(4)=200.          ! maximum pt hat for hard interactions'),
	parameterSets = cms.vstring('pythiaUESettings',
				    'processParameters')
	)
				 )

process.genParticlesForFilter = cms.EDProducer("GenParticleProducer",
					       saveBarCodes = cms.untracked.bool(True),
					       src = cms.InputTag("generator"),
					       abortOnUnknownPDGCode = cms.untracked.bool(True)
					       )


process.ProductionFilterSequence = cms.Sequence(process.generator*process.genParticlesForFilter*process.doubleEMenrichingfilter)

# double reconstructed electrons skim
process.load("MyAnalysis.Skims.doubleElectronFilter_cfi")
process.doubleElectronFilter.nLeptons = 2


# Path and EndPath definitions
process.generation_step = cms.Path(cms.SequencePlaceholder("randomEngineStateProducer"))
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.skim_step = cms.Path(process.doubleElectronFilter)
process.out_step = cms.EndPath(process.output)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.skim_step,process.out_step])
# special treatment in case of production filter sequence  
for path in process.paths: 
    getattr(process,path)._seq = process.ProductionFilterSequence*getattr(process,path)._seq
