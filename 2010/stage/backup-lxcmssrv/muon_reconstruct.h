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

#include "TH1.h"
#include "TH2.h"
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
#include "TTree.h"
#include "/home/abis/CMSSW_2_2_9/src/PhysicsTools/StarterKit/interface/circular_reconstruction.h"
#include "/home/abis/CMSSW_2_2_9/src/PhysicsTools/StarterKit/interface/abis_func.h"

// ---------------------------------------------------------

//
// class declaration
//

class MuonReconstruct : public edm::EDAnalyzer {

    public:
        explicit MuonReconstruct(const edm::ParameterSet&);
        ~MuonReconstruct();

    private:
        virtual void beginJob(const edm::EventSetup&) ;
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob();

        // ----------member data ---------------------------  
        // cuts are defined in the constructor
        double pt_cut, eta_cut;

        //variables to fill trees with interesting data
        double pt, delta_pt;
        double phi, r, eta;

        double d_lin_global, d_circ_global;
        double d_lin_inner, d_circ_inner;
        double ref_x_global, ref_y_global;
        double ref_x_inner, ref_y_inner;
        double d_inner_err, d_global_err;

        int n_muons, n_event, mother_pdgid, grandmother_pdgid;
        double lum;

        double chi2_global, ndf_global;
        double in_rad;


        // map to hold histograms and trees
        std::map<std::string, TTree*> tree_container; 
        const math::XYZPointD PVertex; //Vertex point recostructed with all the tracks (beam spot?)
        const double filter_efficiency;
        const double cross_section;

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
