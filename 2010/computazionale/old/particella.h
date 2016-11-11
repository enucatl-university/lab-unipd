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

#include <iostream>
#include "forza.h"

// =====================================================================================
//        Class:  Particella
//  Description:  
// =====================================================================================
class Particella
{
    public:

        // ====================  LIFECYCLE     =======================================
        Particella(double q0, double q1, double v0, double v1, double m=1);                             // constructor

        // ====================  ACCESSORS     =======================================
        double get_q1() const { return q1; };
        double get_q2() const { return q2; };
        double get_v1() const { return v1; };
        double get_v2() const { return v2; };
        double get_mass() const { return m; };
        void print() const ;

        double energia_meccanica(Forza& forza) const;
        double energia_cinetica() const { return 0.5 * m * (v1 * v1 + v2 * v2); };
            
        // ====================  MUTATORS      =======================================
        // dov'e' dopo un tempo t con approssimazione parabolica?
        void azione(Forza& forza, double t);

        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        //        massa
        double m;
        //      coordinate
        double q1, q2, v1, v2;


}; // -----  end of class Particella  -----
#endif
