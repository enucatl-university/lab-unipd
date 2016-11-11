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

#include "particle.h"

const double Particle::g = 9.8;

Particle::Particle(double q1_, double q2_, double v1_, double v2_, double gamma_, double m_){
    q10 = q1_;
    q20 = q2_;
    v10 = v1_;
    v20 = v2_;
    gamma = gamma_;
    m = m_;
}

double Particle::mechanical_energy(double t){
    return m * g * q2(t) + kinetic_energy(t);
}    

double Particle::q2(double t){
    if (not gamma) return q20 + v20 * t - 0.5 * g * t * t;
    return q20 + (v20 + g / gamma) * (1 - exp(-gamma * t)) / gamma - g * t / gamma;
}    
    
double Particle::v2(double t){
    if (not gamma) return v20 - g * t;
    return (v20 + g / gamma) * exp(-gamma * t) - g / gamma;
}

double Particle::v2_prime(double t){
    if (not gamma) return - g;
    return -gamma * (v20 + g / gamma) * exp(-gamma * t);
}

double Particle::q1(double t){
    if (not gamma) return q10 + v10 * t;
    return q10 + v10 / gamma * (1 - exp(-gamma * t));
} 

double Particle::v1(double t){
    return v10 * exp(-gamma * t);
} 

double Particle::t_range(int n_max, double tol, double t0) {
   double t = t0;
   double t_prev;
   int    iter = 0;

   do {
      iter++;
      t_prev = t;
      t = t_prev - q2(t_prev)/v2(t_prev);
   } while (fabs(t - t_prev) > tol && iter < n_max);

   return t;
}  

double Particle::t_max_height(int n_max, double tol, double t0) {
   double t = t0;
   double t_prev;
   int    iter = 0;

   do {
      iter++;
      t_prev = t;
      t = t_prev - v2(t_prev)/v2_prime(t_prev);
   } while (fabs(t - t_prev) > tol && iter < n_max);

   return t;
}  

double Particle::fric_work_simpson(int n, double t){ //return work as integrated with simpson 3/8
    if (not gamma) return 0;

    int n_intervals = 3 * n;
    int n_points = n_intervals + 1;
    double h = t / n_intervals;

    //calculate work
    double work = 0;
    for (int i = 0; i < n_points; i++) {
        double w;
        //first and last weight
        if (not i) w = .5;
        else if (i == n_points - 1) w = .5;

        //other weights
        else if (i and i % 3) w = 1.5;
        else w = 1;

        double v_square = v1(i * h) * v1(i * h) + v2(i * h) * v2(i * h);
        work += - v_square * w;
    }
    work *= (m * gamma * h * 0.75);
    return work;
}
