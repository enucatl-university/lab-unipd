// =====================================================================================
// 
//       Filename:  drawer.cpp
// 
//    Description:  draw graphs
// 
//        Version:  1.0
//        Created:  16/11/2009 18:36:58
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
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
    cout << "usage:" << endl;
    cout << "t_max, dt, b, f0, omega, method" << endl;
    TApplication app("app", &argc, argv);
    gStyle->SetFillColor(0);

    double t_max, dt, b, f0, omega;

    stringstream arguments;
    stringstream input_name;
    for (int i = 1; i < argc; i++){
        arguments << argv[i] << " ";
        input_name << argv[i] << "_";
    }
    input_name << ".out";

    arguments >> t_max;
    arguments >> dt;
    arguments >> b;
    arguments >> f0;
    arguments >> omega;
    string method;
    arguments >> method;

    TCanvas position_can("position_can", "Position");
    TF1 force("force", "[0] * cos([1] * x)", 0, t_max);
    force.SetParameters(f0, omega);
    force.SetLineColor(2);
    force.SetLineWidth(1);
    force.SetLineStyle(2);
    force.SetNpx(100000);
    TGraph position_graph(input_name.str().c_str(), "%lg %lg %*lg %*lg %*lg");
    position_graph.SetTitle("Position");
    position_graph.GetXaxis()->SetTitle("t");
    position_graph.GetXaxis()->SetRangeUser(0, t_max);
    position_graph.GetYaxis()->SetTitle("x");
    position_graph.GetYaxis()->SetDecimals();
    position_graph.Draw("AP");
    position_can.SaveAs("position_graph.eps");
    if (f0) force.Draw("LSAME");


    TCanvas delta_energy_can("delta_energy_can", "Delta Energy");
    TGraph delta_energy_graph(input_name.str().c_str(), "%lg %*lg %lg %*lg %*lg");
    delta_energy_graph.SetTitle("E_{t} - E_{0}");
    delta_energy_graph.GetXaxis()->SetTitle("t");
    delta_energy_graph.GetXaxis()->SetRangeUser(0, t_max);
    delta_energy_graph.GetYaxis()->SetTitle("#Delta E");
    delta_energy_graph.GetYaxis()->SetDecimals();
    delta_energy_graph.Draw("AP");
    delta_energy_can.SaveAs("delta_energy_graph.eps");

    TCanvas energy_av_can("energy_av_can", "Average Energy");
    TGraph energy_av_graph(input_name.str().c_str(), "%lg %*lg %*lg %lg %*lg");
    energy_av_graph.SetTitle("Average energy per period");
    energy_av_graph.GetXaxis()->SetTitle("t");
    energy_av_graph.GetXaxis()->SetRangeUser(0, t_max);
    energy_av_graph.GetYaxis()->SetTitle("#bar{E}");
    energy_av_graph.GetYaxis()->SetDecimals();

    TCanvas power_av_can("power_av_can", "Average Power");
    TGraph power_av_graph(input_name.str().c_str(), "%lg %*lg %*lg %*lg %lg");
    power_av_graph.SetTitle("Average power transmitted per period");
    power_av_graph.GetXaxis()->SetTitle("t");
    power_av_graph.GetXaxis()->SetRangeUser(0, t_max);
    power_av_graph.GetYaxis()->SetTitle("#bar{P}");
    power_av_graph.GetYaxis()->SetDecimals();

    if (omega and f0){
        energy_av_can.cd();
        energy_av_graph.Draw("AP");

        power_av_can.cd();
        power_av_graph.Draw("AP");

        power_av_can.SaveAs("power_av_graph.eps");
        energy_av_can.SaveAs("energy_av_graph.eps");
    }
    app.Run();
    return 0;
}				// ----------  end of function main  ----------
