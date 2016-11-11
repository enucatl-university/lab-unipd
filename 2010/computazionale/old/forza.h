#ifndef  FORZA_INC
#define  FORZA_INC
// =====================================================================================
// 
//       Filename:  forza.h
// 
//    Description:  classe forza
// 
//        Version:  1.0
//        Created:  06/10/2009 12:07:15
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), webmaster@latinblog.org
//        Company:  
// 
// =====================================================================================

#include "particella.h"

// =====================================================================================
//        Class:  Forza
//  Description:  l
// =====================================================================================

class Forza
{
    public:

        // ====================  LIFECYCLE     =======================================                                
        Forza(double gamma_);       // constructor 
        // ====================  ACCESSORS     =======================================
        double forza1(double q1, double q2, double v1, double v2, double m);
        double forza2(double q1, double q2, double v1, double v2, double m);
        double potenziale(double q1, double q2, double m);

        // ====================  MUTATORS      =======================================

        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        const double g;
        double gamma;

}; // -----  end of class Forza  -----
#endif
