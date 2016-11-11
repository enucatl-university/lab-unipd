{
  TFile * fast = new TFile("GsfTracks.root");
  TFile * full = new TFile("electronZEEFullSim.root");
  // the following should not been changed 
  TString dirName="/DQMData/EgammaV/ElectronMcSignalValidator/";

  // pick-up one of the histograms below
  // The Fast-Full comparison can be found here
  //http://cmsdoc.cern.ch/cms/Physics/egamma/www/validation/351/Electrons/vsFastSim/RelValZEE_Mc/
  //  TString histoName="h_ele_foundHitsVsEta";   // number of hits vs eta.
  //  TString histoName="h_ele_foundHitsVsEta_pfx";  // the same in a Profile
  //  TString histoName="h_ele_dEtaCl_propOut";     // Delta-eta cluster - track-out (should be looked at in log)
  //  TString histoName="h_ele_fbrem";                  //  fbrem=(pin-pout)/pin
  TString histoName="h_ele_outerP_mode";
  TObject * obj=(TObject*)full->Get(dirName+histoName);
  if ( obj->IsA()->InheritsFrom( "TH2" ) )
    {
      TH2F* myH2Fast = (TH2F*)fast->Get(dirName+histoName);
      myH2Fast->SetMarkerColor(2);
      myH2Fast->SetMarkerStyle(23);
      TH2F* myH2Full = (TH2F*)full->Get(dirName+histoName);
      myH2Full->SetMarkerColor(4);
      myH2Full->SetMarkerStyle(22);
      myH2Full->Draw();
      myH2Fast->Draw("same");
    }
  if ( obj->IsA()->InheritsFrom( "TProfile" ) )
    {
      TProfile* myH2Fast = (TProfile*)fast->Get(dirName+histoName);
      myH2Fast->SetLineColor(2);
      TProfile* myH2Full = (TProfile*)full->Get(dirName+histoName);
      myH2Full->SetLineColor(4);
      myH2Full->Draw();
      myH2Fast->Draw("same");
    }
  if ( obj->IsA()->InheritsFrom( "TH1" ) && ! obj->IsA()->InheritsFrom("TH2"))
    {
      // Renormalize the TH1F 
      TH1F* myH1Fast = (TH1F*)fast->Get(dirName+histoName);
      myH1Fast->SetLineColor(2);
      float nfast= myH1Fast->GetEntries();
      TH1F* myH1Full = (TH1F*)full->Get(dirName+histoName);
      float nfull= myH1Full->GetEntries();
      myH1Full->SetLineColor(4);
      myH1Full->Scale(nfast/nfull);
      myH1Full->Draw();
      myH1Fast->Draw("same");
    }
}
