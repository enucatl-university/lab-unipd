// =====================================================================================
// 
//       Filename:  drawer.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  13/12/2009 16:11:00
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis ()jjjjjjjjjjj, matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


#include <iostream>
#include <sstream>
#include <fstream>
#include "TGraph.h"
#include "TF1.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TApplication.h"
#include "TStyle.h"

using namespace std;

int main(int argc, char **argv)
{
    char* input_name = "molecular.out";
    TApplication app("app", &argc, argv);
    gStyle->SetFillColor(0);

    TCanvas position_can("position_can", "position");
    TGraph position_graph(input_name, "%lg %lg %*lg %*lg %*lg");
    position_graph.SetTitle("Position");
    position_graph.GetXaxis()->SetTitle("t");
    position_graph.GetYaxis()->SetTitle("x");
    position_graph.GetYaxis()->SetDecimals();
    position_graph.Draw("AP");
    position_can.SaveAs("position_graph.eps");

    TCanvas delta_energy_can("delta_energy_can", "Delta Energy");
    TGraph delta_energy_graph(input_name, "%lg %*lg %lg %*lg %*lg");
    delta_energy_graph.SetTitle("E_{t} - E_{0}");
    delta_energy_graph.GetXaxis()->SetTitle("t");
    delta_energy_graph.GetYaxis()->SetTitle("#Delta E");
    delta_energy_graph.GetYaxis()->SetDecimals();
    delta_energy_graph.Draw("AP");
    delta_energy_can.SaveAs("delta_energy_graph.eps");

    TCanvas potential_enery_can("potential_enery_can", "potential Energy");
    TGraph potential_enery_raph(input_name, "%lg %*lg %*lg %lg %*lg");
    potential_enery_raph.SetTitle("U_{t}");
    potential_enery_raph.GetXaxis()->SetTitle("t");
    potential_enery_raph.GetYaxis()->SetTitle("U");
    potential_enery_raph.GetYaxis()->SetDecimals();
    potential_enery_raph.Draw("AP");
    potential_enery_can.SaveAs("potential_enery_graph.eps");

    TCanvas kinetic_energy_can("kinetic_energy_can", "kinetic Energy");
    TGraph kinetic_energy_graph(input_name, "%lg %*lg %*lg %*lg %lg");
    kinetic_energy_graph.SetTitle("K_{t}");
    kinetic_energy_graph.GetXaxis()->SetTitle("t");
    kinetic_energy_graph.GetYaxis()->SetTitle("K");
    kinetic_energy_graph.GetYaxis()->SetDecimals();
    kinetic_energy_graph.Draw("AP");
    kinetic_energy_can.SaveAs("kinetic_energy_graph.eps");

    app.Run();
    return 0;
}				// ----------  end of function main  ----------
