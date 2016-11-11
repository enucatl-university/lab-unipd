#ifndef  PARTICELLA_INC
#define  PARTICELLA_INC
// =====================================================================================
// 
//       Filename:  particella.h
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  06/10/2009 11:46:59
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), webmaster@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <cmath>
#include <iostream>

// =====================================================================================
//        Class:  Particle
//  Description:  
// =====================================================================================
class Particle
{
    public:

        // ====================  LIFECYCLE     =======================================
        Particle(double q0, double q1, double v0, double v1, double gamma, double m=1);                             // constructor

        // ====================  ACCESSORS     =======================================

        double q2(double t);
        double v2(double t);
        double v2_prime(double t);
        double q1(double t);
        double v1(double t);
        double mass() const { return m; };

        double mechanical_energy(double t);
        double kinetic_energy(double t) { return 0.5 * m * (v1(t) * v1(t) + v2(t) * v2(t)); };
            
        //newton-raphson algorithm
        double t_max_height(int n_max, double tol, double t0);
        double t_range(int n_max, double tol, double t0);

        //simpson 3/8
        double fric_work_simpson(int n, double t); //return work as integrated with simpson 3/8
        // ====================  MUTATORS      =======================================

        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
        //gravity
        static const double g;
    protected:

    private:
        //        mass
        double m;
        //      coordinates
        double q10, q20, v10, v20, gamma;


}; // -----  end of class Particle  -----
#endif
