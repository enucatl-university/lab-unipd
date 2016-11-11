// =====================================================================================
// 
//       Filename:  solver.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  16/11/2009 12:47:47
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <iostream>
#include <sstream>
#include <fstream>
#include "harmonic_rk4.h"

using namespace std;

int main(int argc, char *argv[])
{
    cout << "usage:" << endl;
    cout << "t_max, dt, b, f0, omega, eu/rk" << endl;
    cout << endl;
    cout << "example:" << endl;
    cout << "./rk 100 0.01 0.2 0.5 1 rk" << endl;
    cout << "will solve the equations with the runge-kutta" << endl;
    cout << "4th order method, from t=0 to t=100, with steps of 0.01" << endl;
    cout << "friction coefficient is 0.2" << endl;
    cout << "external force is 0.5, with a frequency of 1" << endl;

    double t_min = 0;
    double t_max, dt, b, f0, omega;
    string method;

    stringstream arguments;
    stringstream output_name;
    for (int i = 1; i < argc; i++){
        arguments << argv[i] << " ";
        output_name << argv[i] << "_";
    }
    output_name << ".out";
    ofstream output_file(output_name.str().c_str());

    arguments >> t_max;
    arguments >> dt;
    arguments >> b;
    arguments >> f0;
    arguments >> omega;
    arguments >> method;

    vector<double> x;
    x.push_back(1);
    x.push_back(0);

    Runge_Kutta rk(x, b, f0, omega);

    rk.evolve(t_min, t_max, dt, output_file, method);

    cout << "evolution complete." << endl;
    return 0;
}				// ----------  end of function main  ----------
