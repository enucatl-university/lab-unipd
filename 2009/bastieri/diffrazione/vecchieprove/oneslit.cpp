#ifndef ONESLIT
#define ONESLIT
	Double_t *sines = new Double_t[nfound];
	Double_t *integers = new Double_t[nfound];
	for( int i = 0; i < nfound; i++){
// 	cout << i << " " << xpeaks[i] << endl;
	sines[i] = sin( factor*xpeaks[i] );
	integers[i] = (Double_t) i+1;
	}

	TGraph interp( nfound, integers, sines );
{

	TF1 *line1 = new TF1( "line1", "pol1", 0, nfound/2 +0.5 );
	TF1 *line2 = new TF1( "line2","pol1", nfound/2 +0.5 , nfound );
	Double_t *par1 = new Double_t[2];
	Double_t *par2 = new Double_t[2];
	interp.Fit( "line1", "WVR" );
	interp.Fit( "line2", "WVR+" );
	interp.Draw( "AP" );
// 	interp.FitPanel();

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
	delete slits;
	delete line1;
	delete[] par1;
	delete line2;
	delete[] par2;
}

#endif