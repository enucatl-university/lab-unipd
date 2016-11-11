// =====================================================================================
// 
//       Filename:  rotazioni.cpp
// 
//    Description:  Numero di rotazioni nell'algoritmo di Jacobi al variare
//    della dimensione della matrice
// 
//        Created:  13/12/2009 15:34:53
//       Compiler:  g++
// 
//         Author:  Giorgio Bettineschi
// 
// =====================================================================================

#include "jacobi.cpp"
#include <fstream>

double potenziale(double x, double lambda, double alpha);

int main()
{
   double lambda = 4;
   double alpha = 1;
   int n,i,j,nrot;
   double x, h, xj;
   x = 10.;

   ofstream write("rotazioni.dat");
   for ( n = 100; n <= 1000; n += 20 ) {
       h = 2 * x / ((double)n - 1);
       double d[n];
       double **a, **v;
       a = matrix(1,n,1,n);
       v = matrix(1,n,1,n);
//  assegna i valori della matrice a
       for ( i = 1; i <= n; i++) {
           for ( j = 1; j <= n; j++) {
               xj = -x + (j - 1) * h;
               if ( j == i )
                   a[i][j] = 1 / (h * h) + potenziale(xj, lambda, alpha);
               else if ( fabs(i - j) == 1)
                   a[i][j] = - 1. / (2 * h * h);
               else 
                   a[i][j] = 0;
           }
       }
       a[2][1] = a[n - 1][n] = 0;

       jacobi(a,n,d,v,&nrot);
       write << n << "\t" << nrot << endl;
   }
   write.close();

   return 0;
}

double potenziale(double x, double l, double a)
{
    return a*a/2 * l * (l - 1) * ( 0.5 - 1 / (cosh(a*x)*cosh(a*x)) );
}
