// PAT Analysis Template for Padova group
double delta_phi_acute(double delta_phi);

#include "PhysicsTools/StarterKit/interface/muon_reconstruct.h"

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
    PVertex(0.03203, 0.00013, 0),   //Vertex point recostructed with all the tracks (beam spot?)
    filter_efficiency(0.000689),
    cross_section(5.16e10),
    gen_label(iConfig.getUntrackedParameter<edm::InputTag>("genPart")),  // !
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
    n_event = 0;
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
    iEvent.getByLabel(muo_label, muon_handle);
    // --- Copia delle GenP con figli dei Ks e DiF
    edm::Handle<edm::View<reco::GenParticle> > gen_particles;
    iEvent.getByLabel(Ksg4_label, gen_particles);

    //------------START ANALYSIS CODE-------------------------------------------------

    n_muons = muon_handle->end() - muon_handle->begin();  
    n_event++;
    lum = n_event / (cross_section * filter_efficiency);
    for(edm::View<pat::Muon>::const_iterator muon_iter = muon_handle->begin(); muon_iter != muon_handle->end(); ++muon_iter){
        pat::Muon* muon = new pat::Muon(*muon_iter);
        pt = muon->pt();

        //keep tracks with LastStation, |eta|< eta_cut and Pt > pt_cut GeV
        bool muon_is_bad = not(muon->isGood(reco::Muon::TMLastStationOptimizedLowPtTight));
        bool eta_too_big = (fabs(muon->eta()) > eta_cut);
        bool pt_too_small = (pt < pt_cut);
        if (muon_is_bad or eta_too_big or pt_too_small){
            n_muons--;
            continue;
        }

        //find muon-generated particle pair
        reco::GenParticle* gen_particle = find_pair(muon, gen_particles);

        //save r, delta_pt
        r = delta_r(muon, gen_particle);
        delta_pt = relative_delta_pt(muon, gen_particle);

        //fill histograms and trees with R and pt distributions.
        tree_container["r_pt_tree"]->Fill();

        //discard generated-reconstructed pairs if delta pt / pt or R
        //are greater than 0.1
        //skip if track is Null
        bool delta_pt_too_big = (delta_pt > 0.1); 
        bool delta_r_too_big = (r > 0.1); 
        bool track_is_null = (muon->globalTrack().isNull()); 
        if (delta_pt_too_big or delta_r_too_big or track_is_null){
            n_muons--;
            continue;
        }

        //reconstruction of particle track with circular approximation
        CircularReconstruction circ(muon);
        phi = muon->phi();
        ref_x_global = muon->globalTrack()->vx();
        ref_y_global = muon->globalTrack()->vy();
        ref_x_inner = muon->innerTrack()->vx();
        ref_y_inner = muon->innerTrack()->vy();

        //more information:
        //eta, innerposition distance, chi square and ndf
        chi2_global = muon->globalTrack()->chi2();
        ndf_global = muon->globalTrack()->ndof();
        double in_x = muon->globalTrack()->innerPosition().x();
        double in_y = muon->globalTrack()->innerPosition().y();
        in_rad = sqrt(in_x*in_x + in_y*in_y);
        eta = muon->eta();

        //store dxy (absolute value) from reconstructed particle
        //linear and circular approximation
        d_lin_global = fabs(muon->globalTrack()->dxy(PVertex));
        d_circ_global = fabs(circ.impact_parameter_global());
        d_lin_inner = fabs(muon->innerTrack()->dxy(PVertex));
        d_circ_inner = fabs(circ.impact_parameter_inner());

        //error to normalize histograms
        d_inner_err = muon->innerTrack()->dxyError();
        d_global_err = muon->globalTrack()->dxyError();
        //only absolute value is going to be stored in histograms
        //trees still have the signed impact para
        mother_pdgid = 0;
        grandmother_pdgid = 0;

        //if mother or grandmother don't exist, leave the id as 0
        if(gen_particle->mother()){
            mother_pdgid = gen_particle->mother()->pdgId();
            if(gen_particle->mother()->mother()){
                grandmother_pdgid = gen_particle->mother()->mother()->pdgId();
            }
        }

        tree_container["ass_muons"]->Fill();

        delete gen_particle;
        delete muon;
    }
}

// ------------ method called once each job just before starting event loop  ------------
void MuonReconstruct::beginJob(const edm::EventSetup&) {
    edm::Service<TFileService> fs;

    //tree handling
    tree_container["r_pt_tree"] = fs->make<TTree>("r_pt_tree", "Delta R and delta pt / pt tree");
    tree_container["ass_muons"] = fs->make<TTree>("ass_muons", "reco tracks associated to gen particles with delta pt and r");

    //create branches
    //r, deltapt (only first tree)
    tree_container["r_pt_tree"]->Branch("r", &r, "r/D");
    tree_container["r_pt_tree"]->Branch("rel_delta_pt", &delta_pt, "rel_delta_pt/D");

    //make the following branches on all available trees
    abis::make_branch(tree_container, "pt", pt);
    abis::make_branch(tree_container, "phi", phi);
    abis::make_branch(tree_container, "eta", eta);

    abis::make_branch(tree_container, "n_muons", n_muons);
    abis::make_branch(tree_container, "mother_pdgid", mother_pdgid);
    abis::make_branch(tree_container, "grandmother_pdgid", grandmother_pdgid);
    abis::make_branch(tree_container, "n_event", n_event);
    abis::make_branch(tree_container, "lum", lum);

    abis::make_branch(tree_container, "in_rad", in_rad);
    abis::make_branch(tree_container, "chi2_global", chi2_global);
    abis::make_branch(tree_container, "ndf_global", ndf_global);

    abis::make_branch(tree_container, "d_lin_global", d_lin_global);
    abis::make_branch(tree_container, "d_circ_global", d_circ_global);
    abis::make_branch(tree_container, "ref_x_global", ref_x_global);
    abis::make_branch(tree_container, "ref_y_global", ref_y_global);
    abis::make_branch(tree_container, "d_global_err", d_global_err);

    abis::make_branch(tree_container, "d_lin_inner", d_lin_inner);
    abis::make_branch(tree_container, "d_circ_inner", d_circ_inner);
    abis::make_branch(tree_container, "ref_x_inner", ref_x_inner);
    abis::make_branch(tree_container, "ref_y_inner", ref_y_inner);
    abis::make_branch(tree_container, "d_inner_err", d_inner_err);
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
