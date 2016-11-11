#ifndef MALUS
#define MALUS

using namespace std;

class Malus {
	public:
	Malus( char* fileName );
	~Malus();
	Double_t getPhi();
	TH1D* getHist();

	private:
	Int_t lines;
	Double_t* deg;
	Double_t* intensity;
	Double_t* rad;
	TH1D* hPolar;
	TF1 *cos2;
	Double_t phi;
};

Malus::Malus( char* fileName ){
	lines = countLines( fileName );
	deg = new Double_t[lines];
	intensity = new Double_t[lines];
	rad = new Double_t[lines];

	readData( fileName, lines, deg, intensity );

	for( int i = 0; i< lines;i++){
		rad[i] = M_PI / 180 * deg[i];
// 		cout << deg[i] << " " << rad[i] << " " << intensity[i] << endl;
	}

	hPolar = fillHist( lines, deg, intensity );
	cos2 = new TF1( "cos2", "[0]*( cos( [1]*(x-[2]) ) )^2", 1, 50 );
	cos2->SetParameters( 212, M_PI / 180, 25 );
	setStyle( hPolar );
	phi = 0;
}

Malus::~Malus(){
	delete deg;
	delete intensity;
	delete rad;
	delete hPolar;
	delete cos2;
}

Double_t Malus::getPhi(){
	hPolar->Fit( "cos2","R" );
	phi = cos2->GetParameter(2);
// 	cout << cos2->GetParameter(0) << " " << cos2->GetParameter(1);
	return phi;
}

TH1D* Malus::getHist(){
	return hPolar;
}

#endif