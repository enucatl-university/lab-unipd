#include "verlet.h"

Verlet::Verlet(std::vector<double>& init,
                double d_,
                double a_,
                double r0_,
                double m_red){
d = d_;
a = a_;
r0 = r0_;
m = m_red;

x.push_back(init[0]);
v = init[1];

energy_init = energy();
}

double Verlet::morse_potential(double r) const{
    double e = exp(-a * (r - r0));
    return - d * a * e * (2 - e);
    
}
double Verlet::morse_force(double r) const {
    double e = exp(-a * (r - r0));
    return 2 * a * d * e * (e - 1) / m;
}

void Verlet::step(double dt){
    double xt = x[1];
    x[1] = 2 * xt - x[0] + dt * dt * morse_force(xt);
    v = (x[1] - x[0]) / (2 * dt);
    x[0] = xt;
}


void Verlet::evolve(double t_max, double dt,
                std::ostream& os){
    x.push_back(x[0] + v * dt + dt * dt * 0.5 * morse_force(x[0]));

    for (double t = dt; t <= t_max; t += dt) {
        step(dt);
        os << t << " "
            << x[1] - r0 << " "
            << delta_energy() << " "
            << morse_potential(x[1]) << " "
            << kinetic_energy()
            << std::endl;
    }       
}


void dft(std::istream& is, std::ostream& os){
    std::vector<double> input;
    input.reserve(10000);
    double value;
    int i = 0;
    while (is >> value){
        //read second column of input file
        if (i % 5 == 1) input.push_back(value); 
        i++;
    }

    int N = input.size();
    double norm = 1 / (2 * N * M_PI);

    double C = 2 * M_PI / N;
    for (int k = 1; k < N / 2; k++)	 {		/* loop for frequency index */
        //for real input Y_k = Y_{N-k}*, therefore the last N / 2
        //terms are redundant (power spectrum is symmetric).
        double im = 0;
        double re = 0;
        for (int n = 0; n < N; n++)		/* loop for sums */
        {
            re += input[n] * cos(C * n * k);
            im += input[n] * sin(C * n * k);
        }
        double amp = (re * re + im * im) * norm; 
        os << k << " " << amp << std::endl;
    }
}
