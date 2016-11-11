#ifndef FUNCTIONS
#define FUNCTIONS

using namespace std;

int countLines( char* );
Int_t fStep( Double_t*, Int_t );
Int_t lStep( Double_t*, Int_t );
void readData( ifstream, Int_t, Double_t*, Double_t* );
Double_t centerMax( Int_t, Double_t*, Double_t* );
TH1D* fillHist( Int_t, Double_t*, Double_t* );
void setStyle( TH1D* );
void setStyle( TGraph* );

int countLines( char* fileName ){
	ifstream f( fileName, ios_base::in );
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

void readData( char* fileName, Int_t lines, Double_t* step, Double_t* intensity){
	ifstream inData( fileName, ios_base::in );
	for( int i = 0 ; i < lines ; i++ ){
	// read and check for bad data
	inData >> step[i] >> intensity[i];
	if ( (i > 0) && ( abs(intensity[i] - intensity[i-1]) > 50) ) {
		intensity[i] = intensity[i-1];
		}
	}
	inData.close();
	return;
}

Double_t centerMax( Int_t lines , Double_t* step, Double_t* intensity ){
	int maxpos = TMath::LocMax( lines, intensity );
	Int_t maxstep = step[maxpos];
	for( int i = 0 ; i < lines ; i++ ){
		step[i] -=maxstep;
	}
	return maxstep;
}

TH1D* fillHist( Int_t lines , Double_t* step, Double_t* intensity ){
	//draw centered histogram
	int a = 60 + (rand() % 40);
	char ch = (char) a;
	string name = "hist";
	name.append( 1, ch );
	TH1D *hDiff = new TH1D( name.c_str() , "", lines-1, fStep( step, lines ), lStep( step, lines ) );
	for( int i = 0 ; i < lines ; i++ ){
		hDiff->Fill( step[i], intensity[i] );
	}
	return hDiff;
}

void setStyle( TH1D* hDiff ){
	hDiff->GetXaxis()->SetTitle( "angle" );
	hDiff->GetYaxis()->SetTitle( "intensity" );
	hDiff->GetXaxis()->SetTitleSize( 0.03 );
	hDiff->GetYaxis()->SetTitleSize( 0.03 );
	hDiff->GetXaxis()->SetLabelSize( 0.03 );
	hDiff->GetYaxis()->SetLabelSize( 0.03 );
	hDiff->GetYaxis()->SetTitleOffset( 1.2 );
	hDiff->GetXaxis()->SetDecimals(  );
	hDiff->GetYaxis()->SetDecimals(  );
	hDiff->SetStats( kFALSE );
	hDiff->SetTitle( "" );
	return;
}

void setStyle( TGraph* interp ){
	interp->GetXaxis()->SetTitle( "current (A)" );
	interp->GetYaxis()->SetTitle( "delta phi (deg)" );
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