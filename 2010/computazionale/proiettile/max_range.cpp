// =====================================================================================
// 
//       Filename:  max_range.cpp
// 
//    Description:  range as a function of angle
// 
//        Version:  1.0
//        Created:  27/10/2009 17:40:29
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
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

int main(int argc, char **argv){

    TApplication app("app", &argc, argv);

    //pass initial speed from command line
    stringstream arguments;
    arguments << argv[1];

    double speed;
    arguments >> speed;

    ofstream range_stats("range.out");
    //netwon setup
    int n_max = 1000;
    double tol = 1e-7;

    for (int i = 0; i < 90; i++) {
        double angle = i * M_PI / 180;
        double v10 = speed * cos(angle);
        double v20 = speed * sin(angle);
        Particle viscous_part(0, 0, v10, v20, 0.1);
        Particle more_viscous_part(0, 0, v10, v20, 0.3);

        double t_not_viscous = v20 / Particle::g;
        double range_not_viscous = speed * speed / Particle::g * sin(2 * angle);

        double t_range_viscous = viscous_part.t_range(n_max, tol, t_not_viscous);
        double range_viscous = viscous_part.q1(t_range_viscous);

        double t_range_more_viscous = more_viscous_part.t_range(n_max, tol, t_not_viscous);
        double range_more_viscous = more_viscous_part.q1(t_range_more_viscous);

        range_stats << i
            << " " << range_not_viscous
            << " " << range_viscous
            << " " << range_more_viscous << endl; 
    }       
    range_stats.close();

    TGraph not_viscous_g("range.out", "%lg %lg %*lg %*lg");
    TGraph viscous_g("range.out", "%lg %*lg %lg %*lg");
    TGraph more_viscous_g("range.out", "%lg %*lg %*lg %lg");


    TCanvas can("can", "can");
    not_viscous_g.Draw("AP");
    viscous_g.Draw("SAME");
    more_viscous_g.Draw("SAME");

    app.Run();
    return 0;
}
