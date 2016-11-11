// =====================================================================================
// 
//       Filename:  forzato_strang.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  29/11/2009 14:30:50
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include "forzato_strang.h"

Poincare::Poincare(double x_, double v_, int n_steps, double k_){
    x = x_;
    v = v_;
    n = n_steps;
    k = k_;
    h = 2 * M_PI / n_steps;
}

void Poincare::phi1(double dt){
    x += v * dt; //modulo 2 pi
    tau += dt;
}

void Poincare::phi2(double dt){
    v -= (dt * sin(x + dt * v) + k * cos(tau + dt));
}

void Poincare::lie_trotte(){
    x += v * h;
    v -= (h * sin(x + h * v) + k * cos(tau + h));
    tau += h;
}

void Poincare::strang(){
    //2 pi evolution with strang algorithm
    phi2(-h / 2);
    for (int i = 0; i < n; i++) lie_trotte();        
    phi2(h / 2);
}

void Poincare::poincare(int n_points, std::ostream& os){
    os << "{";
    for (int i = 0; i < n_points - 1; i++) {
        tau = 0;
        os << "{" << x << "," << v << "}" << ",";
        strang();
    }       
    os << "{" << x << "," << v << "}" << "}";
}
