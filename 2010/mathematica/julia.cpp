// =====================================================================================
// 
//       Filename:  julia.cpp
// 
//    Description:  
// 
//        Version:  1.0
//        Created:  18/11/2009 17:33:49
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

#include <iostream>
#include <cmath>
#include <vector>

double radius(double cx, double cy);

int main(int argc, char **argv) {
    //cx, cy, ndiv, nit

    double cx, cy;
    int ndiv, nit;
    cin >> cx >> cy >> ndiv >> nit;

    double r = radius(cx, cy);
    double step = 2 * r / ndiv;

    vector<double> ratios;
    ratios.reserve(ndiv * ndiv);


    for (double x = -r; x <= r; x += step) {
        for (double y = -r; y <= r; y += step) {
            int i;
            for (i = 0; i < nit; i++) {
                double a = x;
                double b = y;
                double norm = a * a + b * b;
                if (norm > radius) break;

                double ap = a * a - b * b + ca;
                b = 2 * a * b + cy;
                a = ap;
            }       
            double escape_ratio = static_cast<double>(i) / nit;
            ratios.push_back(escape_ratio);
        }       
    }       

    cout << "{";
    copy(ratios.begin(), ratios.end() - 1, ostream_iterator<double>(cout, ","));
    cout << ratios.back() << "}";
}				// ----------  end of function main  ----------

double radius(double cx, double cy){
    return 1 + sqrt(cx * cx + cy * cy);
}
