
#include <iostream>
#include <iterator>
#include "matrix.h"

using namespace std;

int main(int argc, char **argv) {

    const int n = 6;

    //initialize empty matrix and vector
    mat A(n, vec(n, 0));
    vec b(n, 0), x_g(n,0), x_lu(n, 0);
    mat L, U, I;
    L = U = I = A;

    //non-null entries
    A[0][0] = A[0][3] = A[0][5] = A[1][1] = A[1][4] = A[2][3] = A[2][4] = A[3][3] = A[4][1] = A[5][0] = 1;
    A[1][5] = A[2][2] = A[3][4] = A[3][5] = A[4][2] = A[4][4] = A[5][2] = A[5][3] = -1;
    b[0] = b[1] = 1.5;
    b[2] = 3;

    gauss(A, b, x_g);
    lu_solve(A, b, x_lu);
    invert(A, I);

    cout << "Gauss solution: ";
    copy(x_g.begin(), x_g.end(), ostream_iterator<double>(cout, " "));
    cout << endl;
    
    cout << "LU solution: ";
    copy(x_lu.begin(), x_lu.end(), ostream_iterator<double>(cout, " "));
    cout << endl;
    return 0;
}				// ----------  end of function main  ----------
