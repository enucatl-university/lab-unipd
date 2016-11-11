// =====================================================================================
// 
//       Filename:  ising_model.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  30/10/2009 18:30:27
//       Revision:  none
//       ompiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


#include "ising_model.h"

Ising::Ising(double temp_, double mag_field_, int l_, long unsigned int seed){
    temp = temp_;
    mag_field = mag_field_;
    random_gen.SetSeed(seed);
    l = l_;
    coupling = 1;
    n = l * l;


    w = new double*[17];
    s = new int*[l];

    for (int i = 0; i < 17; i++) w[i] = new double[2];
    for (int i = 0; i < l; i++) s[i] = new int[l];

    //randomly initialize spins
    for (int i = 0; i < l; i++) 
        for (int j = 0; j < l; j++) 
            s[i][j] = 2 * random_gen.Integer(2) - 1; //random 1 or -1

    compute_boltzmann_factors();
}

Ising::~Ising(){
    for (int i = 0; i < 17; i++) delete[] w[i];
    for (int i = 0; i < l; i++) delete[] s[i];
    delete[] w;
    delete[] s;
}

void Ising::compute_boltzmann_factors(){
    int i;
    for (i = -8; i <= 8; i += 4) {
        w[i + 8][0] = exp( - (i * coupling + 2 * mag_field) / temp);
        w[i + 8][1] = exp( - (i * coupling - 2 * mag_field) / temp);
    }
}

bool Ising::metropolis()
{
    // choose a random spin
    int i = random_gen.Integer(l);
    int j = random_gen.Integer(l);

    // find its neighbors using periodic boundary conditions
    int i_prev = (i - 1 + l) % l;
    int i_next = (i + 1) % l;
    int j_prev = (j - 1 + l) % l;
    int j_next = (j + 1) % l;

    // find sum of neighbors
    int sum_neighbors = s[i_prev][j] + s[i_next][j] + s[i][j_prev] + s[i][j_next];
    int delta_ss = 2 * s[i][j] * sum_neighbors;

    // ratio of Boltzmann factors
    double ratio = w[delta_ss + 8] [(1 + s[i][j]) / 2];
    if (random_gen.Uniform() < ratio){
        s[i][j] = -s[i][j];
        return true;
    }
    else return false;
}


void Ising::monte_carlo() {
    for (int i = 0; i < n; i++) metropolis();
}    

void Ising::set_magnetization(int mag){
    for (int i = 0; i < l; i++) 
        for (int j = 0; j < l; j++) 
            s[i][j] = mag; //all spins aligned +1/-1
}

double Ising::magnetization() const {
    int spin_sum = 0;
    for (int i = 0; i < l; i++)
        for (int j = 0; j < l; j++)
            spin_sum += s[i][j];
    return static_cast<double>(spin_sum) / n;
}

double Ising::energy() const {
    int spin_sum = 0; int sspin_sum = 0;
    for (int i = 0; i < l; i++)
        for (int j = 0; j < l; j++){
            spin_sum += s[i][j];
            int i_next = (i + 1) % l;
            int j_next = (j + 1) % l;
            sspin_sum += s[i][j]*(s[i_next][j] + s[i][j_next]);
        }
    return -(coupling * sspin_sum + mag_field * spin_sum) / n;
}     

void Ising::save_complete_sim(int max_steps, ostream& os){
    for (int i = 0; i < max_steps; i++) {
        monte_carlo();
        double mag = magnetization();
        double e = energy();
        //        os << i << " " << e << " " << e * e << " " << mag << mag * mag << std::endl;
        os << e << " " << mag << std::endl;
    }       
}

int Ising::equilibrium_time(int iterations) const {
    std::vector<int> time_vector(iterations, 0);
    for (std::vector<int>::iterator time_it = time_vector.begin(); time_it != time_vector.end(); time_it++) {
        Ising i(temp, mag_field, l);
        i.set_magnetization(1);
        while (i.magnetization() > 0){
            (*time_it)++;
            i.monte_carlo();
        }
    }       
    return *std::max_element(time_vector.begin(), time_vector.end());
}

void Ising::equilibrium_time_mean(int iterations, int& mean, double& rms) const {
    std::vector<int> time_vector(iterations, 0);
    for (std::vector<int>::iterator time_it = time_vector.begin(); time_it != time_vector.end(); time_it++) {
        Ising i(temp, mag_field, l);
        i.set_magnetization(1);
        while (i.magnetization() > 0){
            (*time_it)++;
            i.monte_carlo();
        }
    }       
    mean = TMath::Mean(time_vector.begin(), time_vector.end());
    rms = TMath::RMS(time_vector.begin(), time_vector.end());
}
