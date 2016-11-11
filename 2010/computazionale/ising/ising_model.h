#ifndef  ISING_MODEL_INC
#define  ISING_MODEL_INC
// =====================================================================================
// 
//       Filename:  ising_model.h
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  30/10/2009 18:30:18
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <iostream>
#include <ctime>
#include <cmath>
#include <vector>
#include "TRandom3.h"
#include "TMath.h"

// =====================================================================================
//        Class:  Ising
//  Description:  l
// =====================================================================================
class Ising
{
    public:

        // ====================  LIFECYCLE     =======================================
        Ising(double temp_, double mag_field_, int l, long unsigned int seed=time(NULL));                             // constructor
        ~Ising();

        // ====================  ACCESSORS     =======================================
        double magnetization() const;
        double energy() const;
        int equilibrium_time(int iterations) const; //find eq time as the first time magnetization is zero starting with all spins aligned +1
        void equilibrium_time_mean(int it, int& mean, double& rms) const; //find mean and rms
        //max over iterations long vector

        // ====================  MUTATORS      =======================================
        void set_magnetization(int mag);
        void monte_carlo(); //n = l * l metropolis steps
        bool metropolis();
        void compute_boltzmann_factors();
        void save_complete_sim(int max_steps, ostream& os=std::cout);
        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        double** w;   // Boltzmann factors
        int** s; //spins
        int l, n; //number of spins
        double temp; 
        double mag_field;
        int coupling;
        TRandom3 random_gen;


}; // -----  end of class Ising  -----

#endif // ----- #ifndef ISING_MODEL_INC  -----
