#ifndef SLITCLASS
#define SLITCLASS

using namespace std;

#include "functions.cpp"

class Slit {
// methods for analyzing minima in diffraction pattern, one or more slits.
	public:

	protected: Int_t nfound;
	protected: Float_t *xpeaks;
	protected: Double_t *sines;
	protected: Double_t *integers;
	protected: TGraphErrors *interp;
	protected: Double_t* par1;
	protected: Double_t* par2;
	protected: Double_t* parerr1;
	protected: Double_t* parerr2;
	protected: Double_t* ey;

	Slit( Int_t found, Float_t* peaks );
	~Slit();

	void fillErrors();
	Double_t* getSines();
	Double_t* getIntegers();
	TGraphErrors* getGraph();
	void saveRootFile( TGraphErrors* );
	void setGraphStyle();
	Double_t* weightMean( Double_t*, Double_t* );

	virtual TGraphErrors* drawAndFit();
	virtual Double_t* getSlitWidth();

	private:
};



Slit::Slit( Int_t found, Float_t* peaks ){
	nfound = found;
	xpeaks = new Float_t[nfound];
	memcpy( xpeaks, peaks, nfound*(sizeof *peaks) ); //makes a deep copy in order to avoid memory management problems
	sines = new Double_t[nfound];
	integers = new Double_t[nfound];
	interp = new TGraphErrors;
	par1 = new Double_t[2];
	par2 = new Double_t[2];
	parerr1 = new Double_t[2];
	parerr2 = new Double_t[2];
	ey = new Double_t[nfound];
	fillErrors();
}

Slit::~Slit( ){
	delete sines;
	delete integers;
	delete xpeaks;
	delete interp;
	delete par1;
	delete par2;
	delete parerr1;
	delete parerr2;
}

void Slit::fillErrors(){
	for( int i = 0; i < nfound; i++){
		ey[i] = sqrt( pow( factor*cos(factor*xpeaks[i]),2)*pow(8,2) );
	}
}

Double_t* Slit::weightMean( Double_t* p, Double_t* q){
	Double_t* mean = new Double_t[2];
	mean[0] = ( p[0]/pow( p[1], 2 ) + q[0]/pow( q[1], 2 ) ) / ( 1./pow( p[1], 2 ) + 1./pow( q[1], 2 ) );
	mean[1] = 1 / sqrt( 1./pow( p[1], 2 ) + 1./pow( q[1], 2 ) );
	return mean;
}

Double_t* Slit::getSines(){
	return sines;
}

Double_t* Slit::getIntegers(){
	return integers;
}

	TGraphErrors* Slit::getGraph(){
	return interp;
}

void Slit::saveRootFile( TGraphErrors* h ){
	TFile diffraction( "interp.root","recreate" );
	diffraction.cd();
	getGraph()->Write();
	diffraction.Close();
	return;
}

TGraphErrors* Slit::drawAndFit(){
	return 0;
}

Double_t* Slit::getSlitWidth(){
	return 0;
}

void Slit::setGraphStyle(){
	interp->GetXaxis()->SetTitle( "order" );
	interp->GetYaxis()->SetTitle( "sine" );
	interp->GetYaxis()->SetTitleOffset( 1.2 );
	interp->GetXaxis()->SetTitleSize( 0.03 );
	interp->GetYaxis()->SetTitleSize( 0.03 );
	interp->GetXaxis()->SetLabelSize( 0.03 );
	interp->GetYaxis()->SetLabelSize( 0.03 );
	interp->GetXaxis()->SetDecimals(  );
	interp->GetYaxis()->SetDecimals(  );
// 	interp->SetStats( kFALSE );
	interp->SetTitle( "" );
}

#endif