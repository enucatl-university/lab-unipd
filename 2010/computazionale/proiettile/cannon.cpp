// =====================================================================================
// 
//       Filename:  proiettile.cpp
// 
//    Description:  volo di un proiettile date condizioni iniziali di angolo
//    e velocita'
// 
//        Version:  1.0
//        Created:  06/10/2009 11:43:24
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), webmaster@latinblog.org
//        Company:  
// 
// =====================================================================================


#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <sstream>
#include "particle.cpp"

#include "TApplication.h"
#include "TGraph.h"
#include "TCanvas.h"

using namespace std;

//parse command line options
void set_parameters(int argc, char **argv,
        double& q10, double& q20,
        double& v10, double& v20,
        double& gamma);
void print_usage();

int main(int argc, char **argv)
{
    TApplication app("app", &argc, argv);
    //output files
    string viscous_name = "viscous.out";
    string free_fall_name = "free_fall.out";
    ofstream viscous_file(viscous_name.c_str());
    ofstream free_fall_file(free_fall_name.c_str());

    double gamma, q10, q20, v10, v20;
    set_parameters(argc, argv, q10, q20, v10, v20, gamma);

    Particle viscous_part(q10, q20, v10, v20, gamma);
    Particle free_fall_part(q10, q20, v10, v20, 0);

    double t_without_friction = v20 / Particle::g;
    int n_max = 1000;
    double tol = 1e-7;

    double t_range = viscous_part.t_range(n_max, tol, t_without_friction);
    double t_max_height = viscous_part.t_max_height(n_max, tol, t_without_friction);
    double x_max_height = viscous_part.q1(t_max_height);
    double y_max_height = viscous_part.q2(t_max_height);
    double range = viscous_part.q1(t_range);

    double t_max = 2 * v20 / Particle::g;         //draw graph with gamma=0 timescale
    double dt = 0.01;
    for (double t = 0; t < t_max; t += dt){
        viscous_file << viscous_part.q1(t) << " " << viscous_part.q2(t) << endl;
        free_fall_file << free_fall_part.q1(t) << " " << free_fall_part.q2(t) << endl;
    }

    viscous_file.close();
    free_fall_file.close();

    //draw trajectory graph
    TGraph viscous_graph(viscous_name.c_str());
    TGraph free_fall_graph(free_fall_name.c_str());
    free_fall_graph.Draw("AP");
    viscous_graph.Draw("SAME");

    cout << "range: " << range << endl;
    cout << "max height: (" << x_max_height << ", " << y_max_height << ")" << endl;
    cout << "time max height: " << t_max_height << endl;
    cout << "time max height (without friction): " << v20 / Particle::g << endl;
    int n_intervals = 10;
    double w_fric = viscous_part.fric_work_simpson(n_intervals, t_range);
    cout << "lavoro attrito: " << w_fric << endl;
    cout << "lavoro attrito: " << viscous_part.mechanical_energy(t_range) - viscous_part.mechanical_energy(0) << endl;

    app.Run();

    return 0;
}

void set_parameters(int argc, char **argv,
        double& q10, double& q20,
        double& v10, double& v20,
        double& gamma){
    if (argc < 6) {
        cout << "wrong number of arguments." << endl;
        print_usage();
    }
    stringstream arguments;

    for (int i = 1; i < argc; i++){
        arguments << argv[i] << " ";        
    }

    string vel_coord;
    arguments >> gamma;
    arguments >> q10;
    arguments >> q20;
    arguments >> v10;
    arguments >> v20;

    if (argc == 7) arguments >> vel_coord;

    if (argc == 7 && vel_coord == "deg" or vel_coord == "rad"){
        double theta = v20;
        if (vel_coord == "deg")
            theta *= M_PI / 180;
        double v = v10;
        v10 = v * sin(theta);
        v20 = v * cos(theta);
    }

    cout << "gamma = " << gamma << endl;
    cout << "x0 = " << q10 << endl;
    cout << "y0 = " << q20 << endl;
    cout << "v0x = " << v10 << endl;
    cout << "v0y = " << v20 << endl;
}

void print_usage(){
    cout << "Proiettile.cpp" << endl;
    cout << "command line arguments: " << endl;
    cout << "- gamma, friction coefficient" << endl;
    cout << "- x, y coordinates of starting point" << endl;
    cout << "- vx, vy components of initial velocity" << endl;

    cout << endl;
    cout << "if you prefer choosing initial velocity with polar coordinates," << endl;
    cout << "write speed v and angle theta instead of vx and vy, then specify" << endl;
    cout << "rad if the angle is to be read in radians or deg for degrees" << endl;
}
