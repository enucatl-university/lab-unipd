// =====================================================================================
// 
//       Filename:  circuito.cpp
// 
//    Description:  Risolve un circuito elettrico utilizzando le leggi di
//    Kirchoff per scrivere un sistema lineare
// 
//        Created:  22/11/2009 12:19:38
//       Compiler:  g++
// 
//         Author:  Giorgio Bettineschi
// 
// =====================================================================================

#include <iostream>
#include <cmath>
#include "gauss.cpp"
#include "decomposizioneLU.cpp"

using namespace std;

double* gauss(double**, double*, int);
void decomposizioneLU(double** A, double** L, double** U, int n);
double determinanteU(double** U, int n);
double** inversa(double** L, double** U, int n);

int main()
{
  int i,j,n;
  n = 6;
//  cout <<" Inserisci il numero di equazioni: " << endl;
//  cin >> n;

  double** A = new double*[n];
  for ( i = 0; i < n; i++) 
      A[i] = new double[n];
  double* b = new double[n];

// inizializza matrice nulla
  for ( i = 0; i < n; i += 1 ) {
      for ( j = 0; j < n; j += 1 ) 
          A[i][j] = 0;
      b[i] = 0;
  }
// inserisce valori non nulli della matrice
  A[0][0] = A[0][3] = A[0][5] = A[1][1] = A[1][4] = A[2][3] = A[2][4] = A[3][3] = A[4][1] = A[5][0] = 1;
  A[1][5] = A[2][2] = A[3][4] = A[3][5] = A[4][2] = A[4][4] = A[5][2] = A[5][3] = -1;
  b[0] = b[1] = 1.5;
  b[2] = 3;

  decomposizioneLU(A,L,U,n);
  double* x2 = soluzioneLU(L,U,b,n);
  I = inversa(L,U,n);

// stampa il risultato 
  cout << "x = " << "(";
  for (i = 0; i < n - 1; i++) 
      cout << x[i] << ", ";
  cout << x[n - 1] << ")" << endl;

  cout << "x2 = " << "(";
  for (i = 0; i < n - 1; i++) 
      cout << x2[i] << ", ";
  cout << x2[n - 1] << ")" << endl;

//  cout << endl;
//  for ( i = 0; i < n; i += 1 ) {
//      for ( j = 0; j < n; j += 1 )
//          cout << I[i][j] << "\t";
//      cout << endl;
//  }
//  cout << endl;

// delete
  for ( i = 0; i < n; i++)
      delete [] A[i];
  delete [] A;
  delete [] b;
  delete [] x;
  delete [] x2;
  for ( i = 0; i < n; i++)
      delete [] L[i];
  delete [] L;
  for ( i = 0; i < n; i++)
      delete [] U[i];
  delete [] U;
  for ( i = 0; i < n; i++)
      delete [] I[i];
  delete [] I;

  return 0;
}
