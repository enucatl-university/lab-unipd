#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include "TApplication.h"
#include "TFile.h"
#include "TH1.h"
#include "TNtuple.h"
#include "compare.cpp"

using namespace std;

int main(int argc, char **argv) {
    
    string suffix = ".dat";
    const int n_bins = 128;

    //read arguments from command line:
    //my_bragg file_name n_events first_background_bin
    stringstream args;
    for (int i = 1; i < argc; i++) args << argv[i] << " ";
    string file_name;
    int n_events;
    int background_bin;
    args >> file_name;
    args >> n_events;
    args >> background_bin;

    //open output files
    string root_output_name = file_name + "matteo.root";
    TFile root_output(root_output_name.c_str(), "recreate");
    root_output.cd();

    //create ntuple
    TNtuple ntuple("ntuple", "Bragg_ntuple", "maxC:backg:integr:deltaT:energy_fraction");

    for (int i = 0; i < n_events; i++){
        //read data files
        //file name
        stringstream current_file_name;
        current_file_name << file_name << i << suffix;

        //create a histogram for each file
        TH1S *h1 = new TH1S(current_file_name.str().c_str(), "Bragg", 128, 0, n_bins - 1);
        ifstream current_file(current_file_name.str().c_str());
        int read_bin;
        int j = 1;
        vector<int> vect;
        vect.reserve(n_bins);

        while (current_file >> read_bin) { 
            h1->SetBinContent(j, read_bin);
            vect.push_back(read_bin);
            j++;
        }

        //calculate interesting values from data:
        //background mean
        //integral (energy)
        //bragg maximum
        //delta_t (range)
        //energy_fraction (residual kinetic energy after as a fraction of
        //initial energy [integral])

        float backg = h1->Integral(background_bin, n_bins - 1);
        backg /= (n_bins - background_bin);
        float integr = h1->Integral() - backg * n_bins;
        float bragg_max = h1->GetMaximum() - backg;
        float limit = bragg_max * 0.45 + backg;
        int delta_t = (int) count_if(vect.begin(), vect.end(), GreaterThan(limit));

        int max_location = h1->GetMaximumBin();
        float residual_energy = h1->Integral(0, max_location) - backg * (max_location - 1);
        float energy_fraction = residual_energy / integr;

        //fill ntuple, write and close
        ntuple.Fill(bragg_max, backg, integr, delta_t, energy_fraction);
        h1->Write();
        current_file.close();
        delete h1;
    }
    ntuple.Write();
    root_output.Close();
    return 0;
}				// ----------  end of function main  ----------
