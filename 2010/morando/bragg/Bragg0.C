
Int_t ilevent   = GetIntegerDialog("visualizza 50 eventi da:", 0);
char *f1=GetStringDialog("inserisci il nome del file","gr5_");   

void Braggv(Int_t ilevent, char *filenome){
//questa macro visualizza 50 eventi
    Char_t nomefile1[50];
    Char_t nomehisto[500];
    Char_t tipofile[50];
    strcpy(tipofile,".dat");
    FILE *in;
    
    cout<<"visualizza 50 eventi"<<endl;
  
    TCanvas *signals =new TCanvas("signals","signals",10,10,600,800);
    signals->Divide(5,10); 
    signals->AddExec("tnail","tnail()");
    TCanvas *c2 = new TCanvas("c2","c2",650,10,800,600);
    
    Int_t levent=0;   
    Int_t nlevent=50;   

    levent=ilevent;
    nlevent = 50+levent;
    
      
      //loop di lettura di tutti gli eventi di una misura     
      while (levent<nlevent) {

          if(levent>=0){
        
	  sprintf(nomefile1, "%s%d%s", filenome, levent, tipofile);
              printf("%s", nomefile1);
          sprintf(nomehisto, "%s%d", filenome, levent);}
        
          // opening the data file
          printf("nome file %s\n",nomefile1);
          
          in = fopen(nomefile1, "r");
	  //printf("opening file %s\n", nomefile1);			
	  if(in == NULL) { printf("!!!error opening %s !!!\n", nomefile1); return; }

          TH1S *h1 = new TH1S(nomehisto,"Bragg",128,0,127);
          Int_t cont_ch = 0;
          Int_t nlines = 0;

          unsigned char maxeve=0, caneve=0;
          //creo istogrammi con il segnale 
          while (1) {
          Int_t conten=fscanf(in,"%d",&cont_ch);
          if(conten != 1) break;
  
          h1 -> SetBinContent(nlines,cont_ch);
          nlines++;
          signals->cd(nlevent-levent);
          h1->DrawCopy();
          }
        

        fclose(in);
        levent++;
    }
   return;

 }

 
 void tnail() {
   TPad *selold = 0;
   TPad *sel = (TPad*)gPad->GetSelectedPad();
   Int_t px = gPad->GetEventX();
   Int_t py = gPad->GetEventY();
   if (sel && sel != signals && sel != c2) {
      if (selold) delete selold;
      c2->cd();
      TPad *newpad = (TPad*)sel->Clone();
      newpad->SetLogy(0);
      c2->GetListOfPrimitives()->Add(newpad);
      newpad->SetPad(0,0,1,1);
      selold = newpad;
      c2->Update();
   }
   }
   
void Bragg0(){
    Braggv(ilevent,f1);
    }   