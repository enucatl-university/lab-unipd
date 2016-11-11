#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include "TApplication.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "TSpectrum.h"


using namespace std;

int countLines( char* );
Int_t fStep( Double_t*, Int_t );
Int_t lStep( Double_t*, Int_t );
int minPosition( double* , int, int);
int maxPosition( double* , int, int);
int* interval( double*, int, int );

const double d = 65.5e-3;
const double lambda = 670e-9;
const double lstep = 1.25e-6;
const double factor = lstep/d; //conversion factor from motor steps to angle (rad)
const Double_t integers[8] = { -4, -3, -2, -1, 1, 2, 3, 4 };


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
		if ( (i > 0) && ( abs(intensity[i] - intensity[i-1]) > 50) ) {
		intensity[i] = intensity[i-1];
		}
	}

	//Try to center mean maximum
	int maxpos = maxPosition( intensity, 0, lines );
	Int_t maximum = step[maxpos];
	for( int i = 0 ; i < lines ; i++ ) step[i] -=maximum;

	//trova minimi
	const int limits[9] = {fStep(step,lines),-1700,-1300,-800,0,900,1400,1900,lStep(step,lines)};
	const int n = 8;
	int minimi[n];
	cout << "cerco i minimi..." << endl;
	for( int i = 0; i < n ; i++ ){
		int *lookup = interval( step, limits[i], limits[i+1]);
		cout << "intervallo " << i+1 << ": " << lookup[0] << "-" << lookup[1] << ": ";
		int minPos = minPosition( intensity, lookup[0], lookup[1] );
		minimi[i] = minPos;
		cout << minimi[i] << " " << step[minPos] << endl;
	}
	cout << endl;


	//calculate sines for linear regression
	Double_t sines[n];
	for( Int_t i = 0; i < n ; i++ ){
	sines[i] = factor*step[ minimi[i] ];
// 	cout << step[ minimi[i] ] << " " << sines[i] << endl;
	sines[i] = sin( sines[i] );
// 	cout << integers[i] << " " << sines[i] << endl;
	}
	TGraph interp( n, integers, sines );

	//draw centered histogram
	TH1D hDiff( "hDiff","Diffraction", lines, fStep(step,lines), lStep(step,lines) );
	for( int i = 0 ; i < lines ; i++ )	hDiff.Fill( step[i], intensity[i] );
	TApplication app( "App", &argc, argv );

	TFile bin1("bin1.root","recreate");
	bin1.cd();
	hDiff.Write();
	bin1.Close();

	//data arrays are no longer needed
	delete[] step;
	delete[] intensity;

	//make a copy to draw rebinned histogram
	TH1D hDiff1(hDiff);

// 	TCanvas c1("c1", "Not Yet Rebinned");
// 	hDiff.Draw();
//
// 	TCanvas c2("c2", "Rebinned");
// 	hDiff1.Rebin( 5 );
// 	hDiff1.Draw();

	TCanvas c3("c3", "Sines on minima");
	interp.SetMarkerStyle( kFullDotLarge );
	TF1 *line1 = new TF1("line1","pol1",1,4);
	TF1 *line2 = new TF1("line2","pol1",-4,-1);
	Double_t *par1 = new Double_t[2];
	Double_t *par2 = new Double_t[2];
	interp.Fit("line2","VR");
	interp.Fit("line1","VR+");
	interp.Draw( "AP" );
	//interp.FitPanel();

	//store fitted parameters
	line1->GetParameters(par1);
	line2->GetParameters(par2);

	//print fit results, calculate slit width
	cout << "pendenze trovate: " << endl;
	cout << par1[1] << " " << par2[1] << endl;
	Double_t* slits = new Double_t[2];
	slits[0] = lambda/par1[1];
	slits[1] = lambda/par2[1];
	Double_t slitMean[2] = {(slits[0]+slits[1])/2,abs(slits[0]-slits[1])/2};
	cout << "Larghezza della fenditura = (" << slitMean[0] << " \\pm " << slitMean[1] << ") m" << endl;

	//save on root file
	TFile sinegraph("sines.root","recreate");
	sinegraph.cd();
	interp.Write();
	sinegraph.Close();

	app.Run(kTRUE);

	// memory cleanup

	cout << "memory cleaned" << endl;
	inData.close();
	outData.close();
	delete slits;
	delete line1;
	delete[] par1;
	delete line2;
	delete[] par2;
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
	return min(step[0], step[lines-1]);
}

Int_t lStep( Double_t* step, Int_t lines ){
	return max(step[0], step[lines-1]);
}

int minPosition( double* array, int beg, int end){
	double min = array[beg];
	int minPos = 0;
	for( int i = beg; i < end; i++){
		if ( array[i] < min ) {
		min = array[i];
		minPos = i;
		}
	}
	return minPos;
}

int maxPosition( double* array, int beg, int end){
	double max = array[beg];
	int maxPos = 0;
	for( int i = beg; i < end; i++){
		if ( array[i] > max ) {
		max = array[i];
		maxPos = i;
		}
	}
	return maxPos;
}

int* interval( double* array, int beg, int end){
//finds index interval defined by interval on array items
//array is supposed to be an ordered sequence
	int begIndex = 0;
	int endIndex = 0;
	int *interval = new int[2];
	int i = 0;
	bool notfound1 = true;
	bool notfound2 = true;
	if (array[3] > array[4]){ //decreasing array reverses order
		int a = beg;
		beg = end;
		end = a;
		while( notfound1 || notfound2 ){
			(array[i] > beg)? begIndex = i : notfound1 = false;
			(array[i] > end)? endIndex = i : notfound2 = false;
			i++;
		}
	interval[0] = begIndex;
	interval[1] = endIndex;
	return interval;
	}
	while( notfound1 || notfound2 ){
		(array[i] < beg)? begIndex = i : notfound1 = false;
		(array[i] < end)? endIndex = i : notfound2 = false;
		i++;
	}
	interval[0] = begIndex;
	interval[1] = endIndex;
	return interval;
}