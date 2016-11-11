#ifndef THREESLITS
#define THREESLITS

	const int nslits = 3;
	const int nminima = 2*6*(nslits-1);
	int j = 0;
	while( xpeaks[j] < maxstep ) j++;
	Double_t *chosen = new Double_t[ nminima ];
	for( int i = 0; i < nminima; i++ ){
		chosen[i] = xpeaks[ i + j - nminima/2 - 2 ];
	}

	Double_t *sines = new Double_t[nminima];
	Double_t *integers = new Double_t[nminima];
	j = 0;
	for( int i = 0; i < nminima; i++){
// 	cout << i << " " << xpeaks[i] << endl;
	sines[i] = sin( factor*chosen[i] );
	if ( (i/2 > 0) && (i%2 == 0) ) j++;
	integers[i] = (Double_t) i + j;
	}

	TGraph interp( nminima, integers, sines );

	TF1 *line1 = new TF1( "line1", "pol1", 0, 6*nslits-.5 );
	TF1 *line2 = new TF1( "line2","pol1", 6*nslits , 2*6*nslits );
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
	slits[0] = ( 2*lambda )/( nslits*par1[1] );
	slits[1] = ( 2*lambda )/( nslits*par2[1] );
	Double_t slitMean[2] = {(slits[0]+slits[1])/2,abs(slits[0]-slits[1])/2};
	cout << "Distanza tra le fenditure = (" << slitMean[0] << " \\pm " << slitMean[1] << ") m" << endl;
	delete slits;
	delete line1;
	delete[] par1;
	delete chosen;
	delete line2;
	delete[] par2;


#endif