#ifndef FOURSLITCLASS
#define FOURSLITCLASS

using namespace std;

#include "functions.cpp"
#include "Slit.cpp"

class FourSlit: public Slit {
// methods for analyzing minima in diffraction pattern, one or more slits.
	public:
	FourSlit( Int_t found, Float_t* peaks, Double_t ms );
	TGraphErrors* drawAndFit();
	Double_t* getSlitWidth();
	private:
	Double_t maxstep;
	static const int nslits = 4;
	static const int nminima = 2*6*(nslits-1);
	int j;
	Double_t *chosen;
};



FourSlit::FourSlit( Int_t found, Float_t* peaks, Double_t ms ) : Slit( found, peaks ){
	maxstep = ms;
	j = 0;
	chosen = new Double_t[nminima];
}

// FourSlit::~FourSlit( ){
// }

TGraphErrors* FourSlit::drawAndFit(){
	while( xpeaks[j] < maxstep ) j++;
	for( int i = 0; i < nminima; i++ ){
		chosen[i] = xpeaks[ i + j - nminima/2 - 2 ];
		cout << chosen[i] << endl;
	}
	j = 0;
	for( int i = 0; i < nminima; i++){
// 	cout << i << " " << chosen[i] << endl;
	sines[i] = sin( factor*chosen[i] );
	if ( (i/3 > 0) && (i%3 == 0) ) j++;
	integers[i] = (Double_t) i + j;
	}

	TGraphErrors* g = new TGraphErrors( nminima, integers, sines, 0, ey );
	TF1 *line1 = new TF1( "line1", "pol1", 0, 6*nslits-.5 );
	TF1 *line2 = new TF1( "line2","pol1", 6*nslits , 2*6*nslits );
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

Double_t* FourSlit::getSlitWidth(){
	Double_t* slit1 = new Double_t[2];
	Double_t* slit2 = new Double_t[2];
	slit1[0] = ( lambda )/( nslits*par1[1] );
	slit2[0] = ( lambda )/( nslits*par2[1] );
	slit1[1] = slit1[0]*parerr1[1] / par1[1];
	slit2[1] = slit2[0]*parerr2[1] / par2[1];
	Double_t *slitMean;
	slitMean = weightMean( slit1, slit2 );
	delete slit1;
	delete slit2;
// 	cout << "Slit width = (" << slitMean[0] << " \\pm " << slitMean[1] << ") m" << endl;
	return slitMean;
}


#endif