#ifndef PhysicsTools_StarterKit_MuonReconstruct_h
#define PhysicsTools_StarterKit_MuonReconstruct_h

// standard include files
#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ParameterSet/interface/InputTag.h"


#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "TH1D.h"
#include "TH2D.h"
#include <map>

#include "DataFormats/Common/interface/View.h"
#include <string>

#include "TProfile.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/MuonReco/interface/MuonSelectors.h"  

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h" // OneToOne  
#include "DataFormats/Candidate/interface/CandMatchMap.h"        // OneToMany
#include "DataFormats/Common/interface/AssociationMap.h"

#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefProd.h"
#include "DataFormats/Common/interface/RefVector.h"
#include "DataFormats/Common/interface/RefVectorBase.h"
#include "DataFormats/Common/interface/RefVectorHolder.h"
#include "DataFormats/Common/interface/RefVectorHolderBase.h"

#include "DataFormats/Common/interface/RefBase.h"
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/Common/interface/RefToBaseProd.h"
#include "DataFormats/Common/interface/RefToBaseVector.h"
#include "DataFormats/Common/interface/RefToPtr.h"
#include "DataFormats/Common/interface/RefHolder.h"
#include "DataFormats/Common/interface/RefHolderBase.h"

#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/PatCandidates/interface/GenericParticle.h"

#include <iostream>
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TTree.h"

// User include files

//#include "DataFormats/Common/interface/RefProd.h"
//#include "DataFormats/Common/interface/Ref.h"
//#include "DataFormats/Common/interface/RefVector.h"

// ---------------------------------------------------------

//
// class declaration
//

class MuonReconstruct : public edm::EDAnalyzer {

    public:
        explicit MuonReconstruct(const edm::ParameterSet&);
        ~MuonReconstruct();

    private:
        void beginJob(const edm::EventSetup&) ;
        void analyze(const edm::Event&, const edm::EventSetup&);
        void endJob() ;

        // ----------member data ---------------------------  
        double pt_cut;
        double eta_cut;
        //store interesting data to fill histograms and trees
        double delta_pt;
        double r;
        double d;

        // simple map to contain all histograms. 
        // Histograms are booked in the beginJob() method
        // 1-dimensional
        std::map<std::string, TTree*> tree_container; 

        edm::InputTag gen_label;  
        edm::InputTag ele_label;
        edm::InputTag muo_label;
        edm::InputTag jet_label;
        edm::InputTag tau_label;
        edm::InputTag met_label;
        edm::InputTag pho_label;

        edm::InputTag Ks_label;
        edm::InputTag Lambda_label;
        edm::InputTag Ksg4_label;
};

#endif
