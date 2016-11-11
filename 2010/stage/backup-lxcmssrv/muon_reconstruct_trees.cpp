// PAT Analysis Template for Padova group
double delta_phi_acute(double delta_phi);

#include "PhysicsTools/StarterKit/interface/muon_reconstruct_trees.h"

using namespace std;
reco::GenParticle* find_pair(pat::Muon* muon, edm::Handle<edm::View<reco::GenParticle> > gen_particles);
double delta_r(pat::Muon* muon, reco::GenParticle* gen_p);
double relative_delta_pt(pat::Muon* muon, reco::GenParticle* gen_p);

// constants, enums and typedefs
//
// static data member definitions
//
// constructors and destructor
MuonReconstruct::MuonReconstruct(const edm::ParameterSet& iConfig):
    tree_container(),
    gen_label(iConfig.getUntrackedParameter<edm::InputTag>("genPart")),
    ele_label(iConfig.getUntrackedParameter<edm::InputTag>("electronTag")),
    muo_label(iConfig.getUntrackedParameter<edm::InputTag>("muonTag")),
    jet_label(iConfig.getUntrackedParameter<edm::InputTag>("jetTag")),
    tau_label(iConfig.getUntrackedParameter<edm::InputTag>("tauTag")),
    met_label(iConfig.getUntrackedParameter<edm::InputTag>("metTag")),
    pho_label(iConfig.getUntrackedParameter<edm::InputTag>("photonTag")),
    Ks_label(iConfig.getUntrackedParameter<edm::InputTag>("KsTag")), 
    Lambda_label(iConfig.getUntrackedParameter<edm::InputTag>("LambdaTag")), 
    Ksg4_label(iConfig.getUntrackedParameter<edm::InputTag>("Ksg4Tag"))

{
    //now do what ever initialization is needed
    //cut on muon pt and eta
    pt_cut = 3;
    eta_cut = 2.5;
    //interesting data to store in histograms and trees: relative difference
    //in transverse momentum [delta_pt], distance in (eta, phi) space [r], impact
    //parameter [d].
    delta_pt = 0;
    r = 0;
    d = 0;
}


MuonReconstruct::~MuonReconstruct()
{
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
}


// ------------ method called to for each event  ------------
//
void MuonReconstruct::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    // Muons
    edm::Handle<edm::View<pat::Muon> > muon_handle;
    iEvent.getByLabel(muo_label,muon_handle);
    // --- Copia delle GenP con figli dei Ks e DiF
    edm::Handle<edm::View<reco::GenParticle> > gen_particles;
    iEvent.getByLabel(Ksg4_label,gen_particles);

    //------------START ANALYSIS CODE-------------------------------------------------

    math::XYZPointD PVertex(0.030295, 0.001661, 0);   //Vertex point recostructed with all the tracks (beam spot?)

    for(edm::View<pat::Muon>::const_iterator muon_iter = muon_handle->begin(); muon_iter != muon_handle->end(); ++muon_iter){
        pat::Muon* muon = new pat::Muon(*muon_iter);

        //keep tracks with LastStation, |eta|< eta_cut and Pt > pt_cut GeV
        if (not(muon->isGood(reco::Muon::TMLastStationOptimizedLowPtTight) /*|| true*/)) continue; //modified to include ALL muons!!!
        if (fabs(muon->eta()) > eta_cut or muon->pt() < pt_cut) continue;

        //find muon-generated particle pair
        reco::GenParticle* gen_particle = find_pair(muon, gen_particles);

        //save r, delta_pt
        r = delta_r(muon, gen_particle);
        delta_pt = relative_delta_pt(muon, gen_particle);

        //fill histograms and trees with R and pt distributions.
        
        tree_container["r_pt_tree"]->Fill();

        //discard generated-reconstructed pairs if delta pt / pt or R
        //are greater than 0.1
        if (delta_pt > 0.1 or r > 0.1) continue; 
        //skip if track is Null
        if (muon->track().isNull()) continue;

        //store dxy from reconstructed particle
        d = muon->track()->dxy(PVertex);
        tree_container["d_all_tree"]->Fill();

        //if mother doesn'exist skip track
        if(not(gen_particle->mother())) continue;
        int mother_id = abs(gen_particle->mother()->pdgId()); 

        //in the next histogram only store if mother is a B or D.
        if (mother_id == 521 or mother_id == 411){
            tree_container["d_BD_tree"]->Fill();
            //separate B from D muons and fill different histograms
            if (mother_id == 521){
                tree_container["d_B_tree"]->Fill();
            }
            if (mother_id == 411){
                tree_container["d_D_tree"]->Fill();
            }
        }

        //store Y muons
        if (mother_id == 553 or mother_id == 100553){
                tree_container["d_Y_tree"]->Fill();
        }
        delete gen_particle;
        delete muon;
    }
}

// ------------ method called once each job just before starting event loop  ------------
void MuonReconstruct::beginJob(const edm::EventSetup&) {
    delta_pt = 0;
    r = 0;
    d = 0;
    edm::Service<TFileService> fs;
    //tree handling
    tree_container["r_pt_tree"] = fs->make<TTree>("r_pt_tree_", "Delta R and delta pt / pt tree");
    tree_container["d_all_tree"] = fs->make<TTree>("d_all_tree_", "d from all reco tracks");
    tree_container["d_BD_tree"] = fs->make<TTree>("d_BD_tree_", "d from B or D");
    tree_container["d_B_tree"] = fs->make<TTree>("d_B_tree_", "d from B");
    tree_container["d_D_tree"] = fs->make<TTree>("d_D_tree_", "d from D");
    tree_container["d_Y_tree"] = fs->make<TTree>("d_Y_tree_", "d from Y");
    tree_container["stupid"] = fs->make<TTree>("stupid_", "stupid tree");

    //create branches
    tree_container["r_pt_tree"]->Branch("r", &r, "r/D");
    tree_container["r_pt_tree"]->Branch("delta_pt", &delta_pt, "delta_pt/D");
    tree_container["d_all_tree"]->Branch("d_all", &d, "d_all/D");
    tree_container["d_BD_tree"]->Branch("d_BD", &d, "d_BD/D");
    tree_container["d_B_tree"]->Branch("d_B", &d, "d_B/D");
    tree_container["d_D_tree"]->Branch("d_D", &d, "d_D/D");
    tree_container["d_Y_tree"]->Branch("d_Y", &d, "d_Y/D");
}

// ------------ method called once each job just after ending the event loop  ------------
void MuonReconstruct::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(MuonReconstruct);

double delta_phi_acute(double delta_phi){
    //returns smallest (acute) delta_phi value
    return M_PI - fabs(fabs(delta_phi) - M_PI);
}

reco::GenParticle* find_pair(pat::Muon* muon, edm::Handle<edm::View<reco::GenParticle> > gen_particles){
        //store phi and pt to find closest generated particle
        double reco_phi = muon->phi();
        double reco_eta = muon->eta();
        double R = 1e10;

        //this is going to store the closest particle, while the GenP
        //iterator loops.
        reco::GenParticle *right_particle = new reco::GenParticle;
        //now looping over generated particles
        for(edm::View<reco::GenParticle>::const_iterator gen_p = gen_particles->begin(); gen_p != gen_particles->end(); ++gen_p){
            //pt, eta retrieved for comparison
            double gen_phi = gen_p->phi();
            double gen_eta = gen_p->eta();
            double delta_phi = delta_phi_acute((gen_phi - reco_phi));
            double gen_R = sqrt(delta_phi*delta_phi + (gen_eta - reco_eta)*(gen_eta - reco_eta));
            //look if this particle is a better approximation than the
            //previous ones
            if (gen_R < R){
                R = gen_R;
                *right_particle = reco::GenParticle(*gen_p);
            }
        }
    return right_particle;
}

//find delta r of reco-gen pair
double delta_r(pat::Muon* muon, reco::GenParticle* gen_p){
    double reco_phi = muon->phi();
    double reco_eta = muon->eta();
    double gen_phi = gen_p->phi();
    double gen_eta = gen_p->eta();
    double delta_phi = delta_phi_acute((gen_phi - reco_phi));
    return sqrt(delta_phi*delta_phi + (gen_eta - reco_eta)*(gen_eta - reco_eta));
}

//find delta pt / pt of reco-gen pair
double relative_delta_pt(pat::Muon* muon, reco::GenParticle* gen_p){
    double reco_pt = muon->pt();
    double gen_pt = gen_p->pt();
    return (gen_pt - reco_pt) / gen_pt;
}
