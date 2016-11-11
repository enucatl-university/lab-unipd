#ifndef ONESLITCLASS
#define ONESLITCLASS

using namespace std;

#include "functions.cpp"
#include "Slit.cpp"

class OneSlit: public Slit {
// methods for analyzing minima in diffraction pattern, one or more slits.
	public:
	OneSlit( Int_t found, Float_t* peaks );
	TGraphErrors* drawAndFit();
	Double_t* getSlitWidth();
	private:
};



OneSlit::OneSlit( Int_t found, Float_t* peaks ) : Slit( found, peaks ){
}

// OneSlit::~OneSlit( ){
// }

TGraphErrors* OneSlit::drawAndFit(){
	for( int i = 0; i < nfound; i++){
	cout << i << " " << xpeaks[i] << endl;
	sines[i] = sin( factor*xpeaks[i] );
	integers[i] = (Double_t) i+1;
	}

	TGraphErrors* g = new TGraphErrors( nfound, integers, sines, 0, ey );
	TF1 *line1 = new TF1( "line1", "pol1", 0, nfound/2 +0.5 );
	TF1 *line2 = new TF1( "line2","pol1", nfound/2 +0.5 , nfound );
	g->Fit( "line1", "VR" );
	g->Fit( "line2", "VR+" );
	g->SetMarkerStyle( kFullDotLarge );

	//store fitted parameters
	line1->GetParameters(par1);
	line2->GetParameters(par2);
	parerr1 = line1->GetParErrors();
	parerr2 = line2->GetParErrors();
	interp = g;
	setGraphStyle();
	return interp;
}

Double_t* OneSlit::getSlitWidth(){
	Double_t* slit1 = new Double_t[2];
	Double_t* slit2 = new Double_t[2];
	slit1[0] = lambda/par1[1];
	slit1[1] = slit1[0]*parerr1[1] / par1[1];
	slit2[0] = lambda/par2[1];
	slit2[1] = slit2[0]*parerr2[1] / par2[1];
	Double_t *slitMean;
	slitMean = weightMean( slit1, slit2 );
	delete slit1;
	delete slit2;
// 	cout << "Slit width = (" << slitMean[0] << " \\pm " << slitMean[1] << ") m" << endl;
	return slitMean;
}


#endif