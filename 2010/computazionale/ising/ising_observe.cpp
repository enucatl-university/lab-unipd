#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include "TMath.h"
#include "ising_model.cpp"

using namespace std;

int main(int argc, char **argv) {
    double t_in = 2;
    double t_fin = 2.4;
    double h = 0; //magnetic field

    for (int l = 30; l <= 50; l += 20) { //l = 30, 50
        stringstream ss;
        ss << "observed" << l;
        ofstream os(ss.str().c_str());
        for (double t = t_in; t <= t_fin; t += 0.02) {
            Ising ising(t, h, l);
            int equilibrium_time;

            //below tc a system starting with +1 magnetization will not reach 0.
            //set a default equilibrium time of 1e5
            if (t < 2.27) equilibrium_time = 100000;
            else equilibrium_time = ising.equilibrium_time(100);
            int max_steps = equilibrium_time + 100000;

            vector<double> energy_vector(max_steps, 0);
            vector<double> magnetization_vector(max_steps, 0);

            for (int i = 0; i < max_steps; i++) {
                ising.monte_carlo();
                energy_vector[i] = ising.energy();
                magnetization_vector[i] = ising.magnetization();
            }       

            double energy = TMath::Mean(energy_vector.begin() + equilibrium_time, energy_vector.end());
            double magnetization = TMath::Mean(magnetization_vector.begin() + equilibrium_time, magnetization_vector.end());
            double cv = TMath::RMS(energy_vector.begin() + equilibrium_time, energy_vector.end());
            double chi = TMath::RMS(magnetization_vector.begin() + equilibrium_time, magnetization_vector.end());
            cv *= cv;
            chi *= chi;

            os << t << " " << energy << " " << magnetization << " " << cv << " " << chi << endl;
        }       
        os.close();
    }       
    return 0;
}				// ----------  end of function main  ----------
