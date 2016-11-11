#include "jacobi.cpp"
#include <fstream>

const int l = 4;
const int a = 1;

double potential(double x);

int main(int argc, char **argv) {
    double x = 10;
    int nrot;

   ofstream out("n_rot.out");
   for (int n = 25; n <= 1000; n += 25 ) {
       double h = 2 * x / (n - 1);
       double* d = new double[n];
       double **a, **v;
       a = matrix(1,n,1,n);
       v = matrix(1,n,1,n);
       for (int i = 1; i <= n; i++) {
           for (int j = 1; j <= n; j++) {
               double xj = -x + (j - 1) * h;
               if ( j == i )
                   a[i][j] = 1 / (h * h) + potential(xj);
               else if ( fabs(i - j) == 1)
                   a[i][j] = - 1. / (2 * h * h);
               else 
                   a[i][j] = 0;
           }
       }
       a[2][1] = a[n - 1][n] = 0;

       jacobi(a,n,d,v,&nrot);
       out << n << "\t" << nrot << endl;
   }
   out.close();

   return 0;
}

double potential(double x){
    return a * a * 0.5 * l * (l - 1) * (0.5 - 1 / (cosh(a * x) * cosh(a * x)));
}
