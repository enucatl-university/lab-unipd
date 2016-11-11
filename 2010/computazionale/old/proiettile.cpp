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
#include "particella.cpp"
#include "forza.cpp"
#include "newton.cpp"

#include "TApplication.h"
#include "TGraph.h"
#include "TCanvas.h"

using namespace std;
int main(int argc, char *argv[])
{
    TApplication app("app", &argc, argv);
    double gamma = 0.1;
    Forza gravita(gamma);
    string output_name = "b.out";
    ofstream output(output_name.c_str());
    string output_name_2 = "b2.out";
    ofstream output2(output_name_2.c_str());
    double q10 = 0;
    double q20 = 0;
    double v10 = 3;
    double v20 = 50;
    double dt = 1e-3;
    double t_max = 10;
    Particella part(q10, q20, v10, v20);
    for (double t = 0; t < t_max; t += dt){
        part.azione(gravita, dt);
        output << part.get_q1() << " " << part.get_q2() << endl;
        output2 << x(q10, v10, gamma, t) <<  " " << y(q20, v20, gamma, t) << endl;
    }
    output.close();
    output2.close();

    TCanvas can("can", "can");
    TGraph numeric(output_name.c_str());
    TGraph analitic(output_name_2.c_str());
    numeric.SetLineColor(2);
    numeric.Draw("AP");
    analitic.Draw("SAME");
    int n_max = 1000;
    double tol = 1e-7;
    double t0 = 8;
    double t_gitt = newton(&y, &y_prime, n_max, tol, t0, q20, v20, gamma);
    double gittata = x(q10, v10, gamma, t_gitt);
    double y_fin = y(q20, v20, gamma, t_gitt);
    cout << "gittata: " << gittata << " y finale " << y_fin << endl;
    
    app.Run();
    

    return 0;
}
