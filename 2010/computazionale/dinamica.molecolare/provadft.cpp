// =====================================================================================
// 
//       Filename:  provadft.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  12/12/2009 16:02:23
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis ()jjjjjjjjjjj, matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>
#include "verlet.h"

using namespace std;

const int n = 1000;
const double c = 2 * M_PI / n;
inline double f(double t);

int main(int argc, char **argv) {
    ofstream out("provadft.out");
    for (int i = 0; i < n; i++) {
        out << i << " " <<
            f(i) << " " <<
            0 << " " <<
            0 << " " <<
            0 << " " << endl;
    }       

    out.close();

    ifstream input("provadft.out");
    ofstream transformed("provadftt.out");
    dft(input, transformed);
    transformed.close();
    return 0;
}				// ----------  end of function main  ----------

inline double f(double t){
    return cos(c * t) + 2 * cos(3 * c * t) + 5* cos(5 * c * t);
}
