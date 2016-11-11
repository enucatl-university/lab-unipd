#include <iostream>
#include <cmath>
#include "jacobi2.h"

int main(int argc, char **argv) {
    int n = 3;

    vec d(n, 0);
    mat A(n, vec(n, 0));
    mat eigen_basis = A;

    A[0][0] = A[1][1] = A[2][2] = 2;
    A[0][1] = A[1][0] = 1;
        A[1][2] = A[2][1] = 1;

//    A[0][0] = A[1][1] = 2;
//    A[0][1] = A[1][0] = 1;
//    for (int i = 0; i < n; i++) {
//        for (int j = 0; j < n; j++) {
//            A[i][j] = 0;
//        }
//    }
    Jacobi jac(A);
    jac.get_eigensystem(d, eigen_basis);
    int n_rot = jac.get_n_rot();

    std::cout << "autovalori: " << std::endl;
    for (int i = 0; i < n; i++) { 
        std::cout << d[i] << std::endl;
    }

    std::cout << std::endl;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            std::cout << eigen_basis[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << n_rot << std::endl;
return 0;
}
