#include "matrix.h"
void gauss(mat A, vec b, vec& x) {
    int n = b.size();
    for (int i = 0; i < n - 1; i++) {
        // switch rows until diagonal element is not 0
        int k = i + 1;
        while (not(A[i][i]) && k < n) {
            vec temp = A[i];
            A[i] = A[k];
            A[k] = temp;

            double temp2 = b[i];
            b[i] = b[k];
            b[k] = temp2;
            k++;
        }         

        // subtract row from rows i+1,...,n 
        for (k = i + 1; k < n; k++) {
            double C = A[k][i] / A[i][i];
            for (int j = i; j < n; j++) 
                A[k][j] -= C * A[i][j]; 
            b[k] -= C * b[i];
        }
    }  

    // solve
    for (int k = n - 1; k >= 0; k--) {
        double S = 0;
        for (int i = k + 1; i < n; i++)
            S += A[k][i] * x[i];
        x[k] = (b[k] - S) / A[k][k];
    } 
}

void lu_decomposition(mat& A, mat& L, mat& U) {
    int n = A.size();
    for (int i = 0; i < n; i += 1 ) {
        for (int j = 0; j < n; j += 1 ) {
            L[i][j] = (i == j);
            U[i][j] = 0;
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            double S = 0;
            for (int k = 0; k < i; k++) S += L[i][k] * U[k][j];
            U[i][j] = A[i][j] - S;
        }
        for (int j = i + 1; j < n; j++) {
            double S = 0;
            for (int k = 0; k < i; k++) S += L[j][k] * U[k][i];
            L[j][i] = (A[j][i] - S) / U[i][i];
        }              
    }
}

void lu_solve(mat& A, vec& b, vec& x) {
    int n = A.size();
    mat L(n, vec(n,0));
    mat U = L;
    lu_decomposition(A, L, U);

    vec y(n, 0);

    for (int i = 0; i < n; i++) {
        double sum = 0;
        for (int j = 0; j < i; j++)
            sum += L[i][j] * y[j];
        y[i] = (b[i] - sum) / L[i][i];
    }

    for (int i = n - 1; i >= 0; i--) {
        double sum = 0;
        for (int j = i + 1; j < n; j++)
            sum += U[i][j] * x[j];
        x[i] = (y[i] - sum) / U[i][i];
    }
}

double det_upper(mat& U) {
    int n = U.size();
    double det = 1;
    for (int i = 0; i < n; i++)
        det *= U[i][i];
    return det;
}

void invert(mat& A, mat& I) {
    int n = A.size();
    mat L(n, vec(n,0));
    mat U = L;
    vec e(n, 0);
    vec temp = e;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            e[j] = (j == i);
        lu_solve(A, e, temp);
        for (int j = 0; j < n; j++)
            I[j][i] = temp[j];
    }
}
