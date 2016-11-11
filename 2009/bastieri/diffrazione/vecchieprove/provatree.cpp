#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <cmath>
#include "TApplication.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "TSpectrum.h"
#include "readData.cpp"

using namespace std;

Int_t fStep( TBranch* );
Int_t lStep( TBranch* );
int minimum( TBranch* , int , int );
int maximum( TBranch* , int , int );

// int minPosition( TTree* , char* , int , int );
// int maxPosition( TTree* , char* , int , int );
int* interval( double*, int, int );

const double d = 65.5e-3;
const double lambda = 670e-9;
const double stepLength = 1.25e-6;
const double factor = stepLength/d; //conversion factor from motor steps to angle (rad)
const Double_t integers[8] = { -5, -4, -3, -2, 2, 3, 4, 5 };


int main( int argc, char* argv[] ) {
  char* progname = argv[0];
  cout << " program name: " << progname << endl;
  for ( int i = 1; i < argc; i++ ) {
        cout << " argument n. " << i << " " << argv[i] << endl;
  }
  
  // open file, in read mode, creating ifstream object inData
  char* fileName = argv[1];
  char* outName = argv[2];
  ifstream inData( argv[1], ios::in );
  ofstream outData( argv[2] );
 
  TTree* dataTree = readData( fileName, outName );
  dataTree->SetEstimate(dataTree->GetEntries());

  //draw a histogram
  Int_t lines = (Int_t) dataTree->GetEntries();


  int maxIntAt = maximum( dataTree->GetBranch("y"), 0, 4000 ); //gets central maximum

  Float_t step, intensity;
  dataTree->SetBranchAddress( "x", &step ); //bind variables to tree branches
  dataTree->SetBranchAddress( "y", &intensity );

  Float_t cstep;
  TBranch *centeredSteps = dataTree->Branch( "cstep", &cstep, "cstep/F" );
  dataTree->GetEntry( maxIntAt );
  Float_t centre = step;
  for( int i = 0 ; i< lines ; i++){
    dataTree->GetEntry( i );
    cstep = step - centre;
    centeredSteps->Fill();
  }

  dataTree->Print();

  char* hname = fileName;
  TH1D hDiff( hname,"Diffraction", lines, fStep( dataTree->GetBranch("cstep") ), lStep( dataTree->GetBranch("cstep") ) );
  dataTree->SetBranchAddress( "cstep", &cstep );

  //fill histogram with tree data.
  for( int i = 0 ; i < lines ; i++ ){
    dataTree->GetEntry( i );
    cout << cstep << " " << intensity << endl;
    hDiff.Fill( cstep, intensity );
    hDiff.SetBinError( i, 3 );
  }

  TApplication app( "App", &argc, argv );
  TCanvas c1( "canvas", "Diffraction Pattern" );
  hDiff.Draw("HIST");

  //  TCanvas c2( "can2", "centered pattern" );
  //  dataTree->Draw( "y:cstep", "", "HIST" );
  app.Run(kTRUE);
  // memory cleanup
  delete centeredSteps;
  delete dataTree;
  inData.close();
  outData.close();
  cout << "memory cleaned" << endl;
  return 0;

}

Int_t fStep( TBranch* branch ){
  Long64_t lines = branch->GetEntries();
  Float_t step;
  branch->SetAddress( &step );
  branch->GetEntry( 0 );
  Float_t a = step;
  branch->GetEntry( lines-1 );
  Float_t b = step;
  return min( a, b );
}

Int_t lStep( TBranch* branch ){
  Long64_t lines = branch->GetEntries();
  Float_t step;
  branch->SetAddress( &step );
  branch->GetEntry( 0 );
  Float_t a = step;
  branch->GetEntry( lines-1 );
  Float_t b = step;
  return max( a, b );
}

int minimum( TBranch* branch, int beg = 0, int end = 4000){
  Float_t entry;
  Float_t min = 999999.;
  int minPos = 0;
  branch->SetAddress( &entry );
    for( int i = beg; i < end; i++){
      branch->GetEntry( i );
      if ( entry < min ){
	min = entry;
	minPos = i;
      }
    }
  return minPos;
}

int maximum( TBranch* branch, int beg = 0, int end = 4000){
  Float_t entry;
  Float_t max = -999999.;
  int minPos = 0;
  branch->SetAddress( &entry );
  branch->GetEntry( 1 );
  for( int i = beg + 1; i < end; i++){
    branch->GetEntry( i );
    if ( entry > max ){
      max = entry;
      minPos = i;
    }
  }
  return minPos;
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
