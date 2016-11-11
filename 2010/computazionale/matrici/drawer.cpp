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
    TApplication app("app", &argc, argv);
    gStyle->SetFillColor(0);

    TGraph** eigen_graphs = new TGraph*[3];

    for (int i = 0; i < 3; i++) { 
            stringstream ss;
            ss << "eigen_func_" << i + 1;
            eigen_graphs[i] = new TGraph(ss.str().c_str());
            eigen_graphs[i]->SetTitle("Eigenfunctions");
            eigen_graphs[i]->GetXaxis()->SetTitle("x");
            eigen_graphs[i]->GetYaxis()->SetTitle("#psi(x)");
            eigen_graphs[i]->GetYaxis()->SetDecimals();
            eigen_graphs[i]->GetYaxis()->SetRangeUser(-0.5, 0.5);
            eigen_graphs[i]->GetXaxis()->SetDecimals();
    }

    TGraph potential("potential.out");
    TCanvas eigen_f_can("eigen_f_can", "eigen functions");
    potential.Draw("AP");
    eigen_graphs[0]->Draw("SAME");
    eigen_graphs[1]->Draw("SAME");
    eigen_graphs[2]->Draw("SAME");

    app.Run();
    return 0;
}				// ----------  end of function main  ----------
