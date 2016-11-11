// =====================================================================================
// 
//       Filename:  provavec.cpp
// 
//    Description:  h
// 
//        Version:  1.0
//        Created:  13/12/2009 19:06:13
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <iostream>
#include <vector>

using namespace std;

typedef vector<double> vec;

void scambiavec(vec x, vec& y) {
    x[1] = y[0];
    y[1] = x[0];
}		// -----  end of function scambiavec  -----

int main(int argc, char **argv) {
        vector<double> x(2,1);
        vector<double> y = x;

        cout << "x " << x[0] << " " << x[1] << endl;
        cout << "y " << y[0] << " " << y[1] << endl;

        scambiavec(x, y);
    
        cout << "x " << x[0] << " " << x[1] << endl;
        cout << "y " << y[0] << " " << y[1] << endl;

        return 0;
}				// ----------  end of function main  ----------
