// =====================================================================================
// 
//       Filename:  particella.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  06/10/2009 12:29:21
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), webmaster@latinblog.org
//        Company:  
// 
// =====================================================================================

#include "particella.h"

Particella::Particella(double q1_, double q2_, double v1_, double v2_, double m_){
    q1 = q1_;
    q2 = q2_;
    v1 = v1_;
    v2 = v2_;
    m = m_;
}


void Particella::azione(Forza& forza, double t){
    double a1 = forza.forza1(q1, q2, v1, v2, m) / m;
    double a2 = forza.forza2(q1, q2, v1, v2, m) / m;
    v1 += a1 * t;                          
    v2 += a2 * t;                          
    q1 += v1 * t + 0.5 * a1 * t * t;
    q2 += v2 * t + 0.5 * a2 * t * t;
}

void Particella::print() const{
    std::cout << q1 << " " << q2 << std::endl;
}

double Particella::energia_meccanica(Forza& forza) const{
    return forza.potenziale(q1, q2, m) + energia_cinetica();
}
