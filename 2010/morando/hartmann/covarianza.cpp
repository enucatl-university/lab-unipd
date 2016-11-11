#include <iostream>
#include "TFile.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TFitResult.h"
#include "TF1.h"

int main(int argc, char **argv) {
    
    TGraphErrors hartmann_graph("xl.out");
    TF1 hartmann_fun("hartmann", "[0] + [1] / (x - [2])");
    hartmann_fun.SetParameters(2702.8, -14935288.5, 11494.13);
    hartmann_graph.SetMarkerStyle(8);
    TFitResult r = hartmann_graph.Fit("hartmann", "S");
    return 0;
}				// ----------  end of function main  ----------
