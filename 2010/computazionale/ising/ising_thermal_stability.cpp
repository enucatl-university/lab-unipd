// =====================================================================================
// 
//       Filename:  ising_thermal_stability.cpp
// 
//    Description:  step 2
// 
//        Version:  1.0
//        Created:  03/11/2009 10:08:17
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <iostream>
#include <fstream>
#include <sstream>
#include "TMath.h"
#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TApplication.h"
#include "ising_model.cpp"

using namespace std;

int main(int argc, char **argv) {
    double h = 0; //magnetic field
    double t = 2.5;

    TApplication app("app", &argc, argv);
    stringstream ss;

    int l;
    ss << argv[1];
    ss >> l;
    ofstream en_out("en_out.out");
    ofstream mag_out("mag_out.out");

    Ising ising(t, h, l);
    Ising ising_pos(t, h, l, 3042);
    Ising ising_neg(t, h, l, 2047);
    ising_pos.set_magnetization(1);
    ising_neg.set_magnetization(-1);

    int equilibrium_time = ising.equilibrium_time(50);
    int max_steps = equilibrium_time + 400;

    double e0, m0, e1, m1, e11, m11;

    for (int i = 0; i < max_steps; i++) {
        ising.monte_carlo();
        ising_pos.monte_carlo();
        ising_neg.monte_carlo();

        e0 = ising.energy();
        m0 = ising.magnetization();
        e1 = ising_pos.energy();
        m1 = ising_pos.magnetization();
        e11 = ising_neg.energy();
        m11 = ising_neg.magnetization();

        en_out << i << " " << e0 << " " << e1 << " " << e11 << endl;
        mag_out << i << " " << m0 << " " << m1 << " " << m11 << endl;
    }       
    en_out.close();
    mag_out.close();

    TGraph e0_graph("en_out.out", "%lg %lg %*lg %*lg");
    TGraph e1_graph("en_out.out", "%lg %*lg %lg %*lg");
    TGraph e11_graph("en_out.out", "%lg %*lg %*lg %lg");
    TGraph m0_graph("mag_out.out", "%lg %lg %*lg %*lg");
    TGraph m1_graph("mag_out.out", "%lg %*lg %lg %*lg");
    TGraph m11_graph("mag_out.out", "%lg %*lg %*lg %lg");
    e0_graph.SetMarkerStyle(20);
    m0_graph.SetMarkerStyle(20);

    e1_graph.SetMarkerColor(kRed);
    m1_graph.SetMarkerColor(kRed);
    e1_graph.SetMarkerStyle(22);
    m1_graph.SetMarkerStyle(22);

    e11_graph.SetMarkerColor(kBlue);
    m11_graph.SetMarkerColor(kBlue);
    e11_graph.SetMarkerStyle(23);
    m11_graph.SetMarkerStyle(23);

    stringstream filename_en;
    filename_en << "thermal_stability_en_" << l << ".eps";
    TCanvas en_can("en_can", "en_can");
    e0_graph.SetTitle("energy");
    e0_graph.Draw("AP");
    e1_graph.Draw("PSAME");
    e11_graph.Draw("PSAME");
    en_can.SaveAs(filename_en.str().c_str());

    stringstream filename_mag;
    filename_mag << "thermal_stability_mag_" << l << ".eps";
    TCanvas mag_can("mag_can", "mag_can");
    m0_graph.SetTitle("magnetization");
    m0_graph.Draw("AP");
    m1_graph.Draw("PSAME");
    m11_graph.Draw("PSAME");
    mag_can.SaveAs(filename_mag.str().c_str());
    app.Run();
    return 0;
}				// ----------  end of function main  ----------
