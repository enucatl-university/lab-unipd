
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include "verlet.h"


#include "TApplication.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TAxis.h"

using namespace std;

int main(int argc, char **argv) {
    double d = 0.1679;
    double r0 = 2.409;
    double a = 0.963;
    double m1 = 1836;
    double m2 = 65092;
    double m_red = m1 * m2 / (m1 + m2);

    vector<double> init;
    init.push_back(0.8 * r0);
    init.push_back(0);

    stringstream evolution_par;
    for (int i = 1; i < argc; i++) evolution_par << argv[i] << " ";
    double t_max, dt;
    evolution_par >> t_max;
    evolution_par >> dt;

    ofstream out("molecular.out");

    Verlet molecule(init, d, a, r0, m_red);
    molecule.evolve(t_max, dt, out);

    out.close();

    ifstream input("molecular.out");
    ofstream transformed("dft.out");
    dft(input, transformed);
    transformed.close();

    TApplication app("app", &argc, argv);
    gStyle->SetFillColor(0);
    TCanvas can("can", "can");
    TGraph spectrum("dft.out");
    spectrum.GetXaxis()->SetTitle("n");
    spectrum.GetYaxis()->SetTitle("|Y(#omega)|^{2}");
    can.SetLogy();
    spectrum.GetYaxis()->SetRangeUser(1e-3, 1e3);
    spectrum.Draw("ACP");

    app.Run();

    return 0;
}				// ----------  end of function main  ----------
