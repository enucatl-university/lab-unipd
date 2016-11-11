// =====================================================================================
// 
//       Filename:  ising_equilibrium_time.cpp
// 
//    Description:  find equilibrium time as T -> Tc
// 
//        Version:  1.0
//        Created:  04/11/2009 10:38:57
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
#include <string>
#include <cmath>
#include "TFile.h"
#include "TAxis.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TApplication.h"
#include "ising_model.cpp"

using namespace std;

int main(int argc, char **argv) {
    double l = 30;
    double h = 0; //magnetic field

    TFile output_file("equilibrium_time.root", "recreate");
    TApplication app("app", &argc, argv);
    for (int l = 30; l <= 50; l += 20) { //l = 30, 50
        stringstream graph_file;
        graph_file << "equilibrium_time" << l << ".out";
        ofstream eq_time(graph_file.str().c_str());

        for (double t = 2.50; t >= 2.27; t -= .01) {
            Ising ising(t, h, l);

            int mean_et;
            double rms_et;
            int n_equilibrium_iterations = 200;
            ising.equilibrium_time_mean(n_equilibrium_iterations, mean_et, rms_et);
            eq_time << t << " " << mean_et << " " << 0 << " " << rms_et / sqrt(n_equilibrium_iterations - 1) << endl;
            cout << "temperature = " << t << endl;
        }       
        eq_time.close();
    }

    TCanvas eq_time_can("eq_time", "eq_time");
    TGraphErrors time30("equilibrium_time30.out");
    TGraphErrors time50("equilibrium_time50.out");

    eq_time_can.cd();
    eq_time_can.SetFillColor(0);
    time50.SetMarkerStyle(8);
    time30.SetMarkerStyle(8);
    time50.GetXaxis()->SetDecimals();
    time50.SetMarkerColor(2);
    time50.Draw("AP");
    time30.SetMarkerColor(4);
    time30.Draw("PSAME");

    output_file.cd();
    time30.Write();
    time50.Write();

    output_file.Close();

    app.Run();
    return 0;
}				// ----------  end of function main  ----------
