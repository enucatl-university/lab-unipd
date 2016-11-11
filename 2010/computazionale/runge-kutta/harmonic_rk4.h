#ifndef  HARMONIC_RK4_INC
#define  HARMONIC_RK4_INC
// =====================================================================================
// 
//       Filename:  harmonic_rk4.h
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  16/11/2009 12:45:11
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


#include <vector>
#include <iostream>
#include <cmath>
#include <deque>
#include "TMath.h"

// =====================================================================================
//        Class:  Runge_Kutta
//  Description:  l
// =====================================================================================

double average(std::deque<double> q);

class Runge_Kutta
{
    public:

        // ====================  LIFECYCLE     =======================================
        Runge_Kutta(std::vector<double> x0, double b_=0, double f0_=0, double omega_=0);                             // constructor
        //initial conditions of system of n equations.

        // ====================  ACCESSORS     =======================================
        void print(double t=0, std::ostream& os=std::cout) const;
        double energy_rk() const;
        inline double delta_energy() const { return energy_rk() - energy_ex; };
        double harmonic(std::vector<double> y, unsigned int i, double t=0) const;
        double f(double t) const { return f0 * cos(omega * t); };
        double get_amplitude() const;
        inline double get_power_av() const { return power_av; }

        // ====================  MUTATORS      =======================================
        //single rk step
        //from t to t+dt
        void step(double dt, double t=0);
        void euler_step(double dt, double t=0);

        //evolution from t_min to t_max
        void evolve(double t_min, double t_max, double dt,
                std::ostream& os=std::cout,
                std::string method="rk");

        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        std::vector<double> x;
        double energy_ex, b, f0, omega;

        std::deque<double> energy_period;
        std::deque<double> power_period;
        std::deque<double> amplitude_period;

        int n_period; //intervals in one period of oscillation
        double energy_av;
        double power_av;

}; // -----  end of class Runge_Kutta  -----

#endif // ----- #ifndef HARMONIC_RK4_INC  -----
