
#include "forza.h"

Forza::Forza(double gamma_):
    g(9.8)
{
    gamma = gamma_;
}

double Forza::forza1(double q1, double q2, double v1, double v2, double m){
    
    return -gamma * v1 * m;
}

double Forza::forza2(double q1, double q2, double v1, double v2, double m){
    return -m * (g + gamma * v2);
}

double Forza::potenziale(double q1, double q2, double m){
    return m * g * q2;
}
