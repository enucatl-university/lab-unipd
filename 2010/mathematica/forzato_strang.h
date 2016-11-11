#ifndef  FORZATO_STRANG_INC
#define  FORZATO_STRANG_INC
// =====================================================================================
// 
//       Filename:  forzato_strang.h
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  29/11/2009 14:28:30
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


// =====================================================================================
//        Class:  Poincare
//  Description:  l
// =====================================================================================


#include <iostream>
#include <cmath>

class Poincare
{
    public:

        // ====================  LIFECYCLE     =======================================
        Poincare(double x, double v, int n_steps, double k);                             // constructor

        // ====================  ACCESSORS     =======================================

        // ====================  MUTATORS      =======================================
        void lie_trotte();
        void phi1(double dt);
        void phi2(double dt);
        void strang();
        void poincare(int n_points, std::ostream& os=std::cout);


        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        double x, v, h, k;
        double tau;
        int n;

}; // -----  end of class Poincare  -----

#endif // ----- #ifndef FORZATO_STRANG_INC  -----
