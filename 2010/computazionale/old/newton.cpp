// =====================================================================================
// 
//       Filename:  newton.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  18/10/2009 11:43:43
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


const double g = 9.8;

double y(double y0, double v02, double gamma, double t) ;
double y_prime(double y0, double v02, double gamma, double t);
double y_second(double y0, double v02, double gamma, double t);
double x(double x0, double  v01, double gamma, double t);

double newton(double (*f)(double,double, double, double), double (*f1)(double,double, double, double), int n_max, double tol, double t0, double y0, double v0, double gamma); 



double y(double y0, double v02, double gamma, double t){
    return y0 + (v02 + g / gamma) * (1 - exp(-gamma * t)) / gamma - g * t / gamma;
}    
    
double y_prime(double y0, double v02, double gamma, double t){
    return (v02 + g / gamma) * exp(-gamma * t) - g / gamma;
}

double y_second(double y0, double  v02, double gamma, double t){
    return -gamma * (v02 + g / gamma) * exp(-gamma * t);
}

double x(double x0, double  v01, double gamma, double t){
//    return x0 + v01 / gamma * (1- exp(-gamma * t));
    return x0 + v01 / gamma * (1- exp(-gamma * t));
} 

double newton(double (*f)(double,double, double, double), double (*f1)(double,double, double, double), int n_max, double tol, double t0, double y0, double v0, double gamma) {
   double t = t0;
   double t_prev;
   int    iter = 0;

   do {
      iter++;
      t_prev = t;
      t = t_prev - (*f)(y0, v0, gamma, t_prev)/(*f1)(y0, v0, gamma, t_prev);
   } while (fabs(t - t_prev) > tol && iter < n_max);

   return t;
}  
