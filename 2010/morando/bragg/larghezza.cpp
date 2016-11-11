#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include "TFile.h"
#include "TH1.h"
#include "TNtuple.h"
#include "compare.cpp"

using namespace std;

int main(int argc, char **argv) {
    
    string suffix = ".dat";

    //read arguments from command line:
    //my_bragg pres n_events first_background_bin
    stringstream args;
    for (int i = 1; i < argc; i++) args << argv[i] << " ";
    string pres;
    int n_bins;
    int en_min;
    int en_max;
    args >> pres;
    args >> n_bins;
    args >> en_min;
    args >> en_max;

    stringstream limits_name;
    stringstream integral_hist_name;
    integral_hist_name << "integral_hist" << pres;
    limits_name << pres << "_limits.dat";
    //open output files
    string root_input_name = pres + "_integr.root";
    TFile root_input(root_input_name.c_str());
    TH1I* integral_hist = reinterpret_cast<TH1I*>(root_input.Get(integral_hist_name.str().c_str()));
    int n_entries = integral_hist->GetNbinsX();

    vector<int> entries_vec;
    entries_vec.reserve(n_entries);
    for (int i = 0; i < n_entries; i++) {
        int cont = integral_hist->GetBinContent(i + 1);
        entries_vec.push_back(cont);
    }       

    ifstream limits(limits_name.str().c_str());
    vector<int> limits_vec;
    limits_vec.reserve(6);
    int l;
    while (limits >> l) limits_vec.push_back(l);
    for (int i = 0; i < 6; i++) {
        limits_vec[i] -= en_min;
        limits_vec[i] /= (en_max - en_min) / n_bins;
    }       

    for (int i = 0; i < 6; i + 2) {
        integral_hist->GetXaxis()->SetRange(limits_vec[i], limits_vec[i + 1]);
        double limit = 0.5 * integral_hist->GetMaximum();
        cout << limit << endl;
        int larghezza = (int) count_if(
                entries_vec.begin() + limits_vec[i],
                entries_vec.begin() + limits_vec[i + 1],
                GreaterThan(limit));
        cout << larghezza << endl;
    }       
    root_input.Close();
    return 0;
}				// ----------  end of function main  ----------
