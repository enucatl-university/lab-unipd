#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <algorithm>
#include <cmath>
#include "TApplication.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
#include "TSpectrum.h"

using namespace std;

const double d = 65.5e-3;
const double lambda = 670e-9;
const double lstep = 1.25e-6;
const double factor = lstep/d; //conversion factor from motor steps to angle (rad)

//class definitions
#include "DiffractionData.cpp"
#include "oneSlit.cpp"
#include "twoSlit.cpp"
#include "threeSlit.cpp"
#include "fourSlit.cpp"

int main( int argc, char* argv[] ) {
	char* progname = argv[0];
	cout << " program name: " << progname << endl;
	for ( int i = 1; i < argc; i++ ) {

		cout << " argument n. " << i << " " << argv[i] << endl;
		}

	char* fileName = argv[1];
	char* output = argv[2];
	string graph1 = (string)output + "int.eps";
	string graph2 = (string)output + "sin.eps";

	ofstream o( output );

	TApplication app( "App", &argc, argv );
	DiffractionData data( fileName );

	TCanvas canvas( "intensity", "Intensity / Steps" );
	TSpectrum *s = new TSpectrum( data.getLines() );
	Int_t nfound = s->Search( data.getHist(), 10, "", 0.1 );
	Float_t *xpeaks = s->GetPositionX();
	sort( xpeaks, xpeaks + nfound );

	int slitNumber = argv[3][0] - '0';

	Double_t* slitWidth;
	TGraphErrors* g;
	OneSlit* slit1;
	TwoSlit* slit2;
	ThreeSlit* slit3;
	FourSlit* slit4;

		if ( 1 == slitNumber ){
			slit1 = new OneSlit( nfound, xpeaks );
			g = slit1->drawAndFit();
			slitWidth = slit1->getSlitWidth();
		}
		else if ( 2 == slitNumber ) {
			slit2 = new TwoSlit( nfound, xpeaks );
			g = slit2->drawAndFit();
			slitWidth = slit2->getSlitWidth();
		}
		else if ( 3 == slitNumber ) {
			slit3 = new ThreeSlit( nfound, xpeaks, data.getMaxStep() );
			g = slit3->drawAndFit();
			slitWidth = slit3->getSlitWidth();
		}
		else if ( 4 == slitNumber ) {
			slit4 = new FourSlit( nfound, xpeaks, data.getMaxStep() );
			g = slit4->drawAndFit();
			slitWidth = slit4->getSlitWidth();
		}
		else {
			cout << "Quit." << endl;
			return 0; }
	delete s;

	canvas.SaveAs( graph1.c_str() );

	TCanvas graphCanvas( "graphCanvas", "Sines / integers" );
	g->Draw( "AP" );
	graphCanvas.SaveAs( graph2.c_str() );

	cout << "Slit width or separation is (" << slitWidth[0] << " \\pm " << slitWidth[1] << ") m" << endl;
	o << slitWidth[0] << "\t" << slitWidth[1] << endl;
	o.close();
	cout << "Saved result to " << output << " file" << endl;

	app.Run(kTRUE);
	delete g;
	delete slitWidth;
// 	delete slit1;
// 	delete slit2;
// 	delete slit3;
// 	delete slit4;
	return 0;

}


