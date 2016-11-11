#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <cmath>
#include "TApplication.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
#include "TSpectrum.h"

using namespace std;

int countLines( char* );
Int_t fStep( Double_t*, Int_t );
Int_t lStep( Double_t*, Int_t );

const double d = 65.5e-3;
const double lambda = 670e-9;
const double lstep = 1.25e-6;
const double factor = lstep/d; //conversion factor from motor steps to angle (rad)

int main( int argc, char* argv[] ) {
	char* progname = argv[0];
	cout << " program name: " << progname << endl;
	for ( int i = 1; i < argc; i++ ) {

		cout << " argument n. " << i << " " << argv[i] << endl;
		}


	// open file, in read mode, creating ifstream object inData
	char* fileName = argv[1];
	ifstream inData( argv[1], ios::in );
	ofstream outData( argv[2] );
	Int_t lines = countLines( fileName ); //counts data
	lines -= lines %5;

	Double_t *step = new Double_t[lines];
	Double_t *intensity = new Double_t[lines];

	for( int i = 0 ; i < lines ; i++ ){
		inData >> step[i] >> intensity[i];
		// check for bad data
		if ( (i > 0) && ( abs(intensity[i] - intensity[i-1]) > 50) ) {
		intensity[i] = intensity[i-1];
		}
	}

	//Try to center mean maximum
	int maxpos = TMath::LocMax( lines, intensity );
	Int_t maxstep = step[maxpos];
	for( int i = 0 ; i < lines ; i++ ){
		step[i] -=maxstep;
	}

	//draw centered histogram
	TH1D hDiff( "hDiff","Diffraction", lines, fStep(step,lines), lStep(step,lines) );
	hDiff.GetXaxis()->SetRange( 2 , lines-2 );
	for( int i = 1 ; i <= lines ; i++ ){
		hDiff.Fill( step[i], -intensity[i] );
	}
	TApplication app( "App", &argc, argv );

	TSpectrum s(100);
	Int_t nfound = s.Search( &hDiff, 10, "", 0.05 );
	Float_t *xpeaks = s.GetPositionX();
	sort( xpeaks, xpeaks + nfound );



	TFile diffraction( "diffraction.root","recreate" );
	diffraction.cd();
	hDiff.Write();
	diffraction.Close();

	TCanvas c1( "c1", "Intensity / Steps" );
	hDiff.Draw();

	TCanvas c3( "c3", "Sine" );
	#include "threeslits.cpp"
	interp.SetMarkerStyle( kFullDotLarge );

	//save on root file
	TFile sinegraph( "sines.root", "recreate" );
	sinegraph.cd();
	interp.Write();
	sinegraph.Close();

	app.Run(kTRUE);
	//data arrays are no longer needed
	delete[] step;
	delete[] intensity;
	delete[] sines;
	// memory cleanup
	inData.close();
	outData.close();
	return 0;

}

int countLines( char* filename ){
	ifstream f( filename, ios_base::in );
	if (!f.is_open()) { return 0; }
	int n = 0;
	string t;
	while (getline(f,t)) { n++; }
	f.close();
	return n;
}

Int_t fStep( Double_t* step, Int_t lines ){
	return min( step[0], step[lines-1] );
}

Int_t lStep( Double_t* step, Int_t lines ){
	return max( step[0], step[lines-1] );
}
