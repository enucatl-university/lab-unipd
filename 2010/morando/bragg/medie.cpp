
#include <iostream>
#include <vector>

#include "TMath.h"

using namespace std;

int main(int argc, char **argv) {
    
    vector<double> am, am_w, cm, cm_w, pu, pu_w;

    //energies
    am.push_back(5.388);
    am.push_back(5.48556);
    am.push_back(5.44280);
    cm.push_back(5.76264);
    cm.push_back(5.80477);
    pu.push_back(5.1055);
    pu.push_back(5.1443);
    pu.push_back(5.15659);

    //weights
    am_w.push_back(0.0166);
    am_w.push_back(0.848);
    am_w.push_back(0.131);
    cm_w.push_back(0.2310);
    cm_w.push_back(0.7690);
    pu_w.push_back(0.1194);
    pu_w.push_back(0.1711);
    pu_w.push_back(0.7077);

    double am_mean = TMath::Mean(am.begin(), am.end(), am_w.begin());
    double cm_mean = TMath::Mean(cm.begin(), cm.end(), cm_w.begin());
    double pu_mean = TMath::Mean(pu.begin(), pu.end(), pu_w.begin());
    cout << am_mean << " " << cm_mean << " " << pu_mean << endl;
    return 0;
}				// ----------  end of function main  ----------
