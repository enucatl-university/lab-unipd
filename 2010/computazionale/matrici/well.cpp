
#include <iostream>
#include <cmath>
#include <sstream>
#include <fstream>
#include "jacobi.cpp"

const int l = 4;
const int a = 1;

double potential(double x);

int main(int argc, char **argv) {

    double x = 10;
    int n = 400;
    double h = 2 * x / (n - 1);
    int nrot;

    double* d = new double[n];
    double** a, **v;
    a = matrix(1,n,1,n);
    v = matrix(1,n,1,n);

    ofstream out("potential.out");
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            double xj = -x + (j - 1) * h;
            if (j == i)
                a[i][j] = 1 / (h * h) + potential(xj);
            else if (fabs(i - j) == 1)
                a[i][j] = - 1. / (2 * h * h);
            else 
                a[i][j] = 0;
            out << xj << " " << potential(xj) << endl;
        }
    }

    out.close();

    jacobi(a,n,d,v,&nrot);

    int bounded = 0;
    for (int i = 1; i <= n; i++) { 
        if (d[i] < 3) { 
            bounded++;
            cout << bounded << ": " << d[i] << endl;
            stringstream ss;
            ss << "eigen_func_" << bounded;
            ofstream out(ss.str().c_str());
            for (int j = 1; j <= n; j++) {
                double xj = -x + (j - 1) * h;
                out << xj << " " << v[j][i] << endl;
            }
            out.close();
        }
    }
    cout << "Stati legati: " << bounded << endl;
    cout << "Numero di rotazioni: " << nrot << endl;
    return 0;
}				// ----------  end of function main  ----------

double potential(double x){
    return a * a * 0.5 * l * (l - 1) * (0.5 - 1 / (cosh(a * x) * cosh(a * x)));
}
