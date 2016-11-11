#ifndef  VERLET_INC
#define  VERLET_INC

#include <iostream>
#include <vector>
#include <cmath>

void dft(std::istream& is, std::ostream& os=std::cout);
// =====================================================================================
//        Class:  Verlet
//  Description:  l
// =====================================================================================

class Verlet
{
    public:

        // ====================  LIFECYCLE     =======================================
        Verlet(std::vector<double>& init,
                double d,
                double a,
                double r0,
                double m_red);                             // constructor
        //initial conditions of system of n equations.

        // ====================  ACCESSORS     =======================================
        void print(double t=0, std::ostream& os=std::cout) const;
        double morse_force(double r) const;
        double morse_potential(double r) const;
        inline double energy() const { return kinetic_energy() + morse_potential(x[0]); };
        inline double kinetic_energy() const { return 0.5 * m * v * v; }
        inline double delta_energy() const { return energy() - energy_init; };

        // ====================  MUTATORS      =======================================
        //single verlet step
        //from t to t+dt
        void step(double dt);

        //evolution
        void evolve(double t_max, double dt,
                std::ostream& os=std::cout);

        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        std::vector<double> x;

        double d, a, r0, m, v;
        double energy_init;

}; // -----  end of class Verlet  -----
#endif // ----- #ifndef VERLET_INC  -----
