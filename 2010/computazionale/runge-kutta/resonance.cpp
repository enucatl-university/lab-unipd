// =====================================================================================
// 
//       Filename:  resonance.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  17/11/2009 11:01:47
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
#include "harmonic_rk4.h"
#include "TGraph.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TApplication.h"
#include "TStyle.h"

using namespace std;

int main(int argc, char **argv) {
    cout << "usage:" << endl;
    cout << "t_max, dt, b, f0, omega_max" << endl;
    gStyle->SetFillColor(0);

    TApplication app("app", &argc, argv);
    double omega_min = 0;
    double t_max, dt, b, f0, omega_max;

    stringstream arguments;
    stringstream output_name;
    for (int i = 1; i < argc; i++){
        arguments << argv[i] << " ";
        output_name << argv[i] << "_";
    }
    output_name << "r.out";
    ofstream output_file(output_name.str().c_str());

    arguments >> t_max;
    arguments >> dt;
    arguments >> b;
    arguments >> f0;
    arguments >> omega_max;
    vector<double> x;
    x.push_back(1);
    x.push_back(0);
    ofstream null_stream("/dev/null");

    for (double omega = 0.3; omega <= omega_max; omega += 0.01) {
        Runge_Kutta rk(x, b, f0, omega);
        rk.evolve(0, t_max, dt, null_stream);
        double amp = rk.get_amplitude();
        double power_av = rk.get_power_av();
        output_file << omega << " " << power_av << " " << amp << endl;
    }       

    TCanvas power_freq_can("power_freq_can", "Average Power as a function of frequency");
    TGraph power_freq_graph(output_name.str().c_str(), "%lg %lg %*lg");
    power_freq_graph.SetTitle("Average Power as a function of frequency");
    power_freq_graph.SetMarkerStyle(7);
    power_freq_graph.GetXaxis()->SetTitle("#omega");
    power_freq_graph.GetXaxis()->SetRangeUser(0, t_max);
    power_freq_graph.GetYaxis()->SetTitle("#bar{P}");
    power_freq_graph.GetYaxis()->SetDecimals();
    power_freq_graph.GetXaxis()->SetDecimals();
    power_freq_graph.Draw("AP");
    power_freq_can.SaveAs("power_freq.eps");

    TCanvas amp_can("amp_can", "Amplitude as a function of frequency");
    TGraph amp_graph(output_name.str().c_str(), "%lg %*lg %lg");
    amp_graph.SetTitle("Amplitude as a function of frequency");
    amp_graph.SetMarkerStyle(7);
    amp_graph.GetXaxis()->SetTitle("#omega");
    amp_graph.GetXaxis()->SetRangeUser(0, t_max);
    amp_graph.GetYaxis()->SetTitle("A");
    amp_graph.GetYaxis()->SetDecimals();
    amp_graph.GetXaxis()->SetDecimals();
    amp_graph.Draw("AP");
    amp_can.SaveAs("amp.eps");

    app.Run();
    return 0;
}				// ----------  end of function main  ----------
