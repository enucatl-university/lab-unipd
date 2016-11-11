// =====================================================================================
// 
//       Filename:  forzato.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  29/11/2009 14:51:15
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================


#include <iostream>
#include <sstream>
#include "forzato_strang.h"

int main(int argc, char **argv) {
    
    std::stringstream arguments;
    for (int i = 1; i < argc; i++) arguments << argv[i] << " ";

    double x, v, k;
    int n_steps, n_iterations;

    arguments >> x;
    arguments >> v;
    arguments >> k;
    arguments >> n_steps;
    arguments >> n_iterations;

    Poincare poincare(x, v, n_steps, k);
    poincare.poincare(n_iterations);

    return 0;
}				// ----------  end of function main  ----------
