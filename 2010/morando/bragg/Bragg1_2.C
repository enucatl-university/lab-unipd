{
TFile filenome1 = OpenFileDialog();

   Int_t eventi = ntuple->GetEntries();
   cout<<eventi<<" eventi nella ntupla"<<endl;  
 
   TCanvas *Br1 = new TCanvas("Br1","Analisi",200,10,800,640);

   TPad *pad1 = new TPad("maxC","energia minima",0.02,0.52,0.48,0.98,21);
   TPad *pad2 = new TPad("backg","altra energia",0.52,0.52,0.98,0.98,21);
   TPad *pad3 = new TPad("integr","This is pad3",0.02,0.02,0.48,0.48,21);
   TPad *pad4 = new TPad("deltaT","This is pad4",0.52,0.02,0.98,0.48,21);
   pad1->Draw();
   pad2->Draw();
   pad3->Draw();
   pad4->Draw();
   //
   // Change default style for the statistics box
   gStyle->SetStatW(0.30);
   gStyle->SetStatH(0.20);
   gStyle->SetStatColor(42);
   
   pad1->cd();
   pad1->SetGrid();
   pad1->GetFrame()->SetFillColor(15);
   
   ntuple->Draw("maxC");
   Br1->Update();
  
   pad2->cd();
   pad2->SetGrid();
   pad2->GetFrame()->SetFillColor(32);
   ntuple->SetFillColor(38);
   ntuple->Draw("integr");
   Br1->Update();
   
   pad3->cd();
   pad3->GetFrame()->SetFillColor(38);
   pad3->GetFrame()->SetBorderSize(8);
   ntuple->SetMarkerColor(1);
   ntuple->Draw("backg");
   Br1->Update();
   
   pad4->cd();
   pad4->SetGrid();
   ntuple->Draw("deltaT");
   Br1->cd();
   Br1->Update();
















}