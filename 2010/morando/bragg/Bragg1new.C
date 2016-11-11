
    TNtuple  *ntuple1 = new TNtuple("ntuple1","Bragg_ntuple","levent:maxC:backg:integr:deltaT");
    //TFile *f;
  
    void Braggm(){

//   example of macro to read data from an ascii file and
//   create a root file with an histogram and an ntuple.

char *f1=GetStringDialog("inserisci il nome del file","gr1_500mb_50e");
Int_t ilevent   = GetIntegerDialog("quanti eventi vuoi processare:", 50);
Int_t inifon   = GetIntegerDialog("canale dal quale iniziare a calcolare il fondo:", 70);
    
    Int_t vect[128];	// vettore per i valori di un evento 
    FILE *in;
    Char_t nomefile1[50];
    Char_t nomehisto[500];
    Char_t tipofile[50];
    strcpy(tipofile,".dat");

    
    // warning inserire un check sull'esistenza della radice
    //if(updt==0){
    TString sroot = f1;
    sroot = sroot.Append(".root");
    const char *Fr_nam = sroot.Data();
     // (ri)crea il file per le n-tuple di un determinato set di misure
     TFile *f = new TFile(Fr_nam,"RECREATE");
     if(!f) { printf(" file %s not found",Fr_nam);
         return;}
     //}
    int nlevent = 0;

        
    //prepara una ntupla dove verranno inseriti i valori calcolati dalle curve di Bragg
    // numero evento=levent, maxC=picco di Bragg, backg=background, integr=integrale, deltaT=larghezza al 45%         
    TNtuple *ntuple = new TNtuple("ntuple","Bragg_ntuple","levent:maxC:backg:integr:deltaT");
          
      if(ilevent!=0) {nlevent=ilevent;}
       Int_t  levent=1;
      //printf(" hai selezionato %d eventi\n",ilevent);
      //loop di lettura di tutti gli eventi di una misura     
      while (levent<nlevent) {

          if(levent>0){
	  sprintf(nomefile1, "%s%d%s", f1, levent, tipofile);
          sprintf(nomehisto, "%s%d", f1, levent);}
        
          // opening the data file
          //printf("nome file %s\n",nomefile1);
          in = fopen(nomefile1, "r");
	  printf("opening file %s\n", nomefile1);			
	  if(in == NULL) { printf("!!!error opening %s !!!\n", nomefile1); return 0; }

          TH1S *h1 = new TH1S(nomehisto,"Bragg",128,0,127);
          Int_t cont_ch = 0;
          Int_t nlines = 0;

          unsigned char maxeve=0, caneve=0;
          //creo istogrammi con il segnale 
          while (1) {
          Int_t conten=fscanf(in,"%d",&cont_ch);
          if(conten != 1) break;
          // calcolo del massimo del segnale
          if(cont_ch>maxeve){ maxeve=cont_ch;
          caneve = nlines;}
          vect[nlines] = cont_ch;
    
          h1 -> SetBinContent(nlines,cont_ch);
          nlines++;
          
          }
        
        // calcolo dell'integrale del segnale con fondo sottratto
        Int_t backg=h1->Integral(inifon,127);
        backg /=(128-inifon);
        Int_t intener= h1 -> Integral(0,127);
        intener = intener - backg*128;

        // calcolo della lunghezza dell'evento al 45% del massimo del segnale
        Int_t lowT,upT,limT;
         limT = (maxeve-backg)*0.45+backg;
        for (Int_t jj=caneve; jj<128;jj++){
         if ( vect[jj]>limT) { upT = jj;}}
        for (Int_t jj=0; jj<caneve;jj++){
         if ( vect[jj]<limT) { lowT = jj;}}
    
        Int_t  deltaT = upT-lowT+1;
     
         // printf(" found %d points\n",nlines);
        
         ntuple->Fill(levent,maxeve,backg,intener,deltaT);
        
         ntuple1->Fill(levent,maxeve,backg,intener,deltaT);
        fclose(in);
        levent++;
    }
   f->Write();	// salva la n-tupla su file 
   f->Close();
// ================================================================================================

//	salvataggio in un file dei parametri inseriti dall'utente per la macro successiva

   FILE *backup = fopen("Bragg1.par","w");
   fprintf(backup,"%s\n%d\n%d\n",Fr_nam,levent,inifon);
   fclose(backup);
    
   return;
}


void Braggu(){

TFile filenome2 = OpenFileDialog();
char *f2=GetStringDialog("inserisci la radice del nome del file di dati","gr1_");   
TString ppp = f2;
  //  cout<<f2<<endl;
Int_t ilevent   = GetIntegerDialog("quanti eventi vuoi processare:", 200);
Int_t idevent   = GetIntegerDialog("da quale evento:",0);
Int_t inifon   = GetIntegerDialog("canale dal quale iniziare a calcolare il fondo:", 70);
    //TNtuple  *ntuple = gROOT->FindObject("ntuple1");//new TNtuple("ntuple","Bragg_ntuple","levent:maxC:backg:integr:deltaT");          
    Int_t vect[128];	// vettore per i valori di un evento 
    FILE *in;
    Char_t nomefile2[50];
    Char_t nomehisto[500];
    Char_t tipofile[50];
    strcpy(tipofile,".dat");
 
    //Numero di eventi già presenti nelle ntupla del file aperto
    Int_t eventi=ntuple->GetEntries();    
    filenome2.ReOpen("UPDATE");
    
    int nlevent = 0;
        
    //prepara una ntupla dove verranno inseriti i valori calcolati dalle curve di Bragg

      if(ilevent!=0) {nlevent=ilevent+idevent;}
       Int_t  levent=idevent;

      printf(" hai selezionato %d eventi\n",ilevent);
      //loop di lettura di tutti gli eventi di una misura
      
      
      while (levent<nlevent) {
          if(levent>=0){
	  sprintf(nomefile2, "%s%d%s", f2, levent, tipofile);
          sprintf(nomehisto, "%s%d", f2, levent);}
        
          // opening the data file
          in = fopen(nomefile2, "r");
	  printf("opening file %s\n", nomefile2);			
	  if(in == NULL) { printf("!!!error opening %s !!!\n", nomefile2); return; }

          TH1S *h1 = new TH1S(nomehisto,"Bragg",128,0,127);
          Int_t cont_ch = 0;
          Int_t nlines = 0;

          unsigned char maxeve=0, caneve=0;
          //creo istogrammi con il segnale 
          while (1) {
          Int_t conten=fscanf(in,"%d",&cont_ch);
          if(conten != 1) break;
          // calcolo del massimo del segnale
          if(cont_ch>maxeve){ maxeve=cont_ch;
          caneve = nlines;}
          vect[nlines] = cont_ch;
    
          h1 -> SetBinContent(nlines,cont_ch);
          nlines++;
          
          }
        
        // calcolo dell'integrale del segnale con fondo sottratto
        Int_t backg=h1->Integral(inifon,127);
        backg /=(128-inifon);
        Int_t intener= h1 -> Integral(0,127);
        intener = intener - backg*128;

        // calcolo della lunghezza dell'evento al 45% del massimo del segnale
        Int_t lowT,upT,limT;
         limT = (maxeve-backg)*0.45+backg;
        for (Int_t jj=caneve; jj<128;jj++){
         if ( vect[jj]>limT) { upT = jj;}}
        for (Int_t jj=0; jj<caneve;jj++){
         if ( vect[jj]<limT) { lowT = jj;}}
    
        Int_t  deltaT = upT-lowT+1;
     
        // printf(" found %d points\n,nlines);
        ntuple->Fill(levent,maxeve,backg,intener,deltaT);
        ntuple1->Fill(levent,maxeve,backg,intener,deltaT);
        fclose(in);
        levent++;
    }
   filenome2.Write();	// salva la n-tupla su file filenome1->Write();	
   filenome2.Close(); 
}






void preanalisi(TNtuple *ntuple1){
// ===============================================================================================
//	rappresentazione dei dati  
//	1 Canvas con 4 istogrammi

   TCanvas *Br1 = new TCanvas("Br1","Canvas Bragg Picco-Integrali",200,10,800,640);

   TPad *pad1 = new TPad("maxC","energia minima",0.02,0.52,0.48,0.98,21);
   TPad *pad2 = new TPad("backg","altra energia",0.52,0.52,0.98,0.98,21);
   TPad *pad3 = new TPad("integr","This is pad3",0.02,0.02,0.48,0.48,21);
   TPad *pad4 = new TPad("levent","This is pad4",0.52,0.02,0.98,0.48,21);
   pad1->Draw();
   pad2->Draw();
   pad3->Draw();
   pad4->Draw();
   //
   // Change default style for the statistics box
   gStyle->SetStatW(0.30);
   gStyle->SetStatH(0.20);
   gStyle->SetStatColor(42);
   //
   // Display a function of one ntuple column imposing a condition
   // on another column.
   pad1->cd();
   pad1->SetGrid();
   pad1->GetFrame()->SetFillColor(15);
   ntuple1->SetLineColor(1);
   ntuple1->SetFillStyle(1001);
   ntuple1->SetFillColor(45);
   ntuple1->Draw("maxC:levent");
   Br1->Update();
   //
   // Display the profile of two columns
   // The profile histogram produced is saved in the current directory with
   // the name hprofs

   pad2->cd();
   pad2->SetGrid();
   pad2->GetFrame()->SetFillColor(32);
   ntuple1->SetFillColor(38);
   ntuple1->Draw("integr:levent");
   Br1->Update();
   //
   // Display a scatter plot of two columns with a selection.
   // Superimpose the result of another cut with a different marker color
   pad3->cd();
   pad3->GetFrame()->SetFillColor(38);
   pad3->GetFrame()->SetBorderSize(8);
   ntuple1->SetMarkerColor(1);
   ntuple1->Draw("maxC");
   // ntuple->Draw("py:px","pz<1","same");
   Br1->Update();
   //
   pad4->cd();
   pad4->SetGrid();
   ntuple1->Draw("integr");
   Br1->cd();
   Br1->Update();


   //	 2Â° Canvas con altri 4 istogrammi

   TCanvas *Br2 = new TCanvas("Br2","Canvas Bragg DeltaT-Integrali",200,10,800,640);

   pid1 = new TPad("maxC","energia minima",0.02,0.52,0.48,0.98,21);
   pid2 = new TPad("backg","altra energia",0.52,0.52,0.98,0.98,21);
   pid3 = new TPad("integr","This is pad3",0.02,0.02,0.48,0.48,21);
   pid4 = new TPad("levent","This is pid4",0.52,0.02,0.98,0.48,21);
   pid1->Draw();
   pid2->Draw();
   pid3->Draw();
   pid4->Draw();
   //
   // Change default style for the statistics box
   gStyle->SetStatW(0.30);
   gStyle->SetStatH(0.20);
   gStyle->SetStatColor(42);
   //
   // Display a function of one ntuple column imposing a condition
   // on another column.
   pid1->cd();
   pid1->SetGrid();
   // pid1->SetLogy();
   pid1->GetFrame()->SetFillColor(15);
   ntuple1->SetLineColor(1);
   ntuple1->SetFillStyle(1001);
   ntuple1->SetFillColor(45);
   ntuple1->Draw("deltaT:levent");
   // ntuple1->SetFillColor(5);
   Br2->Update();
   //
   // Display the profile of two columns
   // The profile histogram produced is saved in the current directory with
   // the name hprofs

   pid2->cd();
   pid2->SetGrid();
   pid2->GetFrame()->SetFillColor(32);
   ntuple1->SetFillColor(38);
   ntuple1->Draw("maxC:integr");
   Br2->Update();
   //
   // Display a scatter plot of two columns with a selection.
   // Superimpose the result of another cut with a different marker color
   pid3->cd();
   pid3->GetFrame()->SetFillColor(38);
   pid3->GetFrame()->SetBorderSize(8);
   
   TH1S *hdeltaT = new TH1S("hdeltaT","deltaT",100,0,99);
   ntuple1->Draw("deltaT>>hdeltaT");
   hdeltaT ->SetMarkerColor(1);
   hdeltaT -> Draw();
   Br2->Update();
   //
   pid4->cd();
   pid4->SetGrid();
   ntuple1->Draw("integr");
   Br2->cd();
   Br2->Update();
   
 }

 void Bragg1new(){ 

Braggm();     
Char_t ris;     
cout<<"vuoi aggiungere altri dati?(y/n)"<<endl;
ris=cin.get();

     
switch(ris){
    case 'y': Braggu(); 
    case 'n': cout<<"ok"<<endl;    
        }   
    preanalisi(ntuple1);
    //f->Close();    
     }
