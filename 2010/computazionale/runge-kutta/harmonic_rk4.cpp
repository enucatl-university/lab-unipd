// =====================================================================================
// 
//       Filename:  harmonic_rk4.cpp
// 
//    Description:  :bn
//
// 
//        Version:  1.0
//        Created:  16/11/2009 12:47:43
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include "harmonic_rk4.h"
                   
double average(std::deque<double> q){
    //integral with first order polynomial approximation
    std::vector<double> w(q.size(), 1);
    w.front() = w.back() = 0.5;
    return TMath::Mean(q.begin(), q.end(), w.begin());
}


Runge_Kutta::Runge_Kutta(std::vector<double> x_, double b_, double f0_, double omega_){
    x = x_;
    energy_ex = 0.5*(x[0]*x[0] + x[1]*x[1]);
    b = b_;
    f0 = f0_;
    omega = omega_;

    energy_av = 0;
    power_av = 0;

}

double Runge_Kutta::harmonic(std::vector<double> y, unsigned int i, double t) const {
   if (i == 0) return(y[1]);               // RHS of first equation 
   if (i == 1) return(-y[0] - b * y[1] + f0 * cos(omega * t));              // RHS of second equation 
};

void Runge_Kutta::step(double dt, double t){
    double h = dt / 2; //midpoint
    int n = static_cast<int>(x.size());

    std::vector<double> q1(x), q2(x), q3(x),                // temporary storage 
                        k1(n,0), k2(n,0), k3(n,0),k4(n,0);  // for Runge-Kutta  

   for (int i = 0; i < n; i++) q1[i] += 0.5 * (k1[i] = dt * harmonic(x, i, t));
   for (int i = 0; i < n; i++) q2[i] += 0.5 * (k2[i] = dt * harmonic(q1, i, t + h));
   for (int i = 0; i < n; i++) q3[i] += (k3[i] = dt * harmonic(q2, i, t + h));
   for (int i = 0; i < n; i++) k4[i] = dt * harmonic(q3, i, t + dt);
      
   for (int i = 0; i < n; i++) x[i] += (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6;

    //add new data
    energy_period.push_back(energy_rk());
    power_period.push_back(f(t) * x[1]);
    amplitude_period.push_back(x[0]);

    if (energy_period.size() > n_period) energy_period.pop_front();
    if (power_period.size() > n_period) power_period.pop_front();
    if (amplitude_period.size() > n_period) amplitude_period.pop_front();

    energy_av = average(energy_period);
    power_av = average(power_period);
}

void Runge_Kutta::euler_step(double dt, double t){
    int n = x.size();
    std::vector<double> dx(n, 0);
    for (int i = 0; i < n; i++) dx[i] = dt * harmonic(x, i, t);
    for (int i = 0; i < n; i++) x[i] += dx[i];
}

void Runge_Kutta::evolve(double t_min, double t_max, double dt, std::ostream& os, std::string method){
    //evolve with runge-kutta (rk) or euler (eu)
   
    if (omega and f0) {
    //number of intervals in one period
    //will be used to calculate average energy or power per period
    double period = 2 * M_PI / (omega * dt);
    n_period = static_cast<int>(period) + 1;
    }
    else {
        double omega = sqrt(1 - 0.25 * b * b);
        double period = 2 * M_PI / (omega * dt);
        n_period = static_cast<int>(period) + 1;
    }

    void (Runge_Kutta::*step_function)(double, double) = NULL;
    if (method == "rk") step_function = &Runge_Kutta::step;
    else if (method == "eu") step_function = &Runge_Kutta::euler_step;

    for (double t = t_min; t <= t_max; t += dt) {
        (*this.*step_function)(dt, t);
        print(t, os);
    }       
}

double Runge_Kutta::get_amplitude() const {
    double max_x = *std::max_element(amplitude_period.begin(), amplitude_period.end());
    double min_x = *std::min_element(amplitude_period.begin(), amplitude_period.end());
    double amp = max_x - min_x;
    return amp;
}

double Runge_Kutta::energy_rk() const {
    return 0.5*(x[0]*x[0] + x[1]*x[1]);
}

void Runge_Kutta::print(double t, std::ostream& os) const {
    os << t << " "
        << x[0] << " "
        << delta_energy() << " "
        << energy_av << " "
        << power_av
        << std::endl;
}
