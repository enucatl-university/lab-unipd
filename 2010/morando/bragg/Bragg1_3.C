//gROOT->Reset();
TFile file1;
//TNtuple *ntuple;
// ===============================================================================================
void Bragga(){
    TFile file1 = OpenFileDialog();
    Int_t min   = GetIntegerDialog("minimo dell'intervallo di energia:",0);
    Int_t max   = GetIntegerDialog("massimo dell'intervallo di energia:",10000);

    
    //TNtuple *ntuple1=gROOT->FindObject("ntuple");
    //if (!ntuple){cout<<"file not open"<<endl;
    //    return;
   // }
   Int_t eventi = ntuple->GetEntries();
   cout<<eventi<<" eventi nella ntupla"<<endl;  
 
// ================================================================================================
   const char limit[30];
   sprintf(limit,"integr>%d && integr<%d",min,max);
 
   c1 = new TCanvas("c1","Spettri con filtro sull'energia",10,40,800,600);
   c1->Range(0,0,25,18);
   c1->SetFillColor(40);
   pada = new TPad("pada","This is pad1",0.02,0.02,0.48,0.83,33);
   padb = new TPad("padb","This is pad2",0.52,0.02,0.98,0.83,33);

   pada->Draw();
   padb->Draw();

   TH1F *hdelt = new TH1F("hdelt","DeltaT",60,5.5,70.5); 
   TH1F *hmaxC = new TH1F("hmaxC","MaxBragg",100,53.5,252.5);
   
   pada->cd();
   ntuple->SetMarkerColor(1);
   ntuple->Draw("deltaT>>hdelt",limit);
   c1->Update();
   padb->cd();
   ntuple->SetMarkerColor(1);
   ntuple->Draw("maxC>>hmaxC",limit);
   c1->Update();

   return;
 }


 void Bragg1_3(){
     Bragga();
 }
