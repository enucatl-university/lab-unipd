using namespace std;
#if !defined(__CINT__) || defined(__MAKECINT__)
#include <iostream>
#include <fstream>
#include <TMath.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TF1.h>
#include <TLatex.h>
#endif

Double_t fitfun1(Double_t *x,Double_t *par)
{
 return par[0]+par[1]*x[0];
}

Double_t fitfun2(Double_t *x,Double_t *par)
{
 return par[0]+par[1]*x[0];
}



int main()
{
 gROOT->Reset();
 TCanvas *c1 = new TCanvas("ca","lettura dati",10,10,750,600);

 ifstream fin("dada.dat",ios_base::in);
 fin.open("spettro.preamp.dat");
 const int k= 9;
 double a,b,c;
 int i=0;
 TMultiGraph *sa = new TMultiGraph();
 TGraph *gr1 = new TGraph();
 TGraph *gr2 = new TGraph();

 if(fin.is_open())
 {
   while(i<k)
   {
    fin>>a>>b>>c;
    gr1->SetPoint(i,a,c);
    gr2->SetPoint(i,b,c);
    i++;
   }
 }
 fin.close();


 //sa->SetTitle("spettro amp");
 gr1->SetLineColor(4);
 gr2->SetLineColor(2);
 gr1->SetMarkerStyle(2);
 gr2->SetMarkerStyle(5); 
 TF1 *fit1 = new TF1("fit1",fitfun1,0,1,2); 
 TF1 *fit2 = new TF1("fit2",fitfun2,1,6,2);
 fit1->SetLineWidth(1);
 fit2->SetLineWidth(2);
 gr1->Fit(fit1,"R");
 
 gr2->Fit(fit2,"R");
 sa->Add(gr1);
 sa->Add(gr2);
 c1->SetFillColor(10);

 gStyle->SetOptFit(1);
 sa->Draw("AOP");

   c1->Update();
   TPaveStats *stats1 = (TPaveStats*)gr1->GetListOfFunctions()->FindObject("stats");
   TPaveStats *stats2 = (TPaveStats*)gr2->GetListOfFunctions()->FindObject("stats");
   stats1->SetFillColor(0);
   stats2->SetFillColor(0);
   stats1->SetTextColor(kBlue); 
   stats2->SetTextColor(kRed); 
   stats1->SetX1NDC(0.12); stats1->SetX2NDC(0.32); stats1->SetY1NDC(0.85);
   stats2->SetX1NDC(0.72); stats2->SetX2NDC(0.92); stats2->SetY1NDC(0.85);
   c1->Modified();

 return 0;
}
