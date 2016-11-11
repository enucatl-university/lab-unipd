#ifndef SHIFTFIT
#define SHIFTFIT

using namespace std;

class shiftFitter {
	public:
	shiftFitter( Double_t*, Double_t* );
	~shiftFitter();
	TGraph* getGraph();
	Double_t* getFitParameters();
	Double_t getVerdet();

	private:
	static const double mu0 = 4*M_PI*1e-7;
	static const double ls = 0.18;
	static const double lv = 0.11;
	static const int N = 3660;
	TF1* line;
	TGraph* g;
	Double_t* par;
	Double_t verdet;
};

shiftFitter::shiftFitter( Double_t* current, Double_t* phi ){
	line = new TF1( "line", "pol1", 0, 3 );
	g = new TGraph( 4, current, phi );
	g->Fit( "line", "VR" );
	g->SetMarkerStyle( kFullDotLarge );
	par = new Double_t[2];
	line->GetParameters(par);
	verdet = -( M_PI*par[1]*ls ) / ( 180*mu0*N*lv );
}

shiftFitter::~shiftFitter(){
	delete line;
	delete g;
	delete par;
}

Double_t* shiftFitter::getFitParameters(){
	return par;
}

Double_t shiftFitter::getVerdet(){
	return verdet;
}

TGraph* shiftFitter::getGraph(){
	return g;
}

#endif