#ifndef DIFFDATA
#define DIFFDATA

using namespace std;

#include "functions.cpp"

class DiffractionData {
// stores diffraction data read from file in two Double_t arrays, fills a histogram ready to be analysed by TSpectrum.
	public:
	DiffractionData( char* );
	~DiffractionData();
	Double_t* getSteps();
	Double_t* getIntensity();
	Double_t getMaxStep();
	Int_t getLines();
	TH1D* getHist();
	void saveRootFile( TH1D* );

	private:
	Int_t lines;
	Double_t *step;
	Double_t *intensity;
	Double_t maxstep;
	TH1D *hDiff;
};



DiffractionData::DiffractionData( char* fileName ){
	lines = countLines( fileName );
	step = new Double_t[lines];
	intensity = new Double_t[lines];

	readData( fileName, lines, step, intensity );
	maxstep = centerMax( lines, step, intensity );
	hDiff = fillHist( lines, step, intensity );

	//draw options
	hDiff->GetXaxis()->SetTitle( "step" );
	hDiff->GetYaxis()->SetTitle( "- log intensity" );
	hDiff->GetXaxis()->SetTitleSize( 0.03 );
	hDiff->GetYaxis()->SetTitleSize( 0.03 );
	hDiff->GetXaxis()->SetLabelSize( 0.03 );
	hDiff->GetYaxis()->SetLabelSize( 0.03 );
	hDiff->GetYaxis()->SetTitleOffset( 1.2 );
	hDiff->GetXaxis()->SetDecimals(  );
	hDiff->GetYaxis()->SetDecimals(  );
	hDiff->SetStats( kFALSE );
	hDiff->SetTitle( "" );
}

DiffractionData::~DiffractionData( ){
	delete step;
	delete intensity;
	delete hDiff;
}

Double_t* DiffractionData::getSteps(){
	return step;
}

Double_t* DiffractionData::getIntensity(){
	return intensity;
}

Double_t DiffractionData::getMaxStep(){
	return maxstep;
}

TH1D* DiffractionData::getHist(){
	return hDiff;
}

Int_t DiffractionData::getLines(){
	return lines;
}

void DiffractionData::saveRootFile( TH1D* h ){
	TFile diffraction( "diffraction.root","recreate" );
	diffraction.cd();
	getHist()->Write();
	diffraction.Close();
	return;
}


#endif