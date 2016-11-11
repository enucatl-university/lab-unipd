#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include "TMath.h"
#include "TApplication.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"

using namespace std;

#include "functions.cpp"
#include "Malus.cpp"
#include "shiftFitter.cpp"


Double_t current[4] = { 0, 1, 2, 3 };
Double_t phi[4];

int main( int argc, char* argv[] ) {
	char* progname = argv[0];
	cout << " program name: " << progname << endl;
	for ( int i = 1; i < argc; i++ ) {
		cout << " argument n. " << i << " " << argv[i] << endl;
	}

	char* fileName[4];
	fileName[0] = argv[1];
	fileName[1] = argv[2];
	fileName[2] = argv[3];
	fileName[3] = argv[4];

	Malus** malus = new Malus*[4];

	TApplication app( "App", &argc, argv );
	TCanvas** canvas = new TCanvas*[4];

	for( int i = 0; i < 4; i++){
		int a = 60 + (rand() % 40);
		char ch = (char) a;
		string name = "can";
		name.append( 1, ch );

		cout << fileName[i] << endl;
		canvas[i] = new TCanvas( name.c_str(), name.c_str() );
		malus[i] = new Malus( fileName[i] );
		malus[i]->getHist()->Draw();
		phi[i] = malus[i]->getPhi();
	}

	shiftFitter s( current, phi );
	TCanvas interp( "angle fit", "phase shift (difference)" );
	TGraph *g;
	g = s.getGraph();
	g->Draw( "AP" );

	Double_t verdet = s.getVerdet();


	cout << "Coefficiente di Verdet = " << verdet << " rad / (T m)" << endl;

	app.Run( kTRUE );
	for( int i = 0; i < 4; i++){
		delete malus[i];
		delete canvas[i];
	}
	delete[] canvas;
	delete[] malus;
// 	delete g;

	return 0;
}