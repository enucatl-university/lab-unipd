#include "eigen.h"

int jacobi(mat& A, vec& lambda, mat& eigen_basis){
    double thresh, theta, tau, t, s, h, c;

    int n = A.size();
    vec b(n, 0);
    vec z = b;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            eigen_basis[i][j] = 0; 
        eigen_basis[i][i] = 1;
    }

    for (int i = 0; i < n; i++) 
        b[i] = lambda[i] = A[i][i];

    int n_rot = 0;
    for (int counter = 0; counter < 100; counter++) {
        double sm = 0;
        for (int i = 0; i < n - 1; i++) 
            for (int j = i + 1; j < n; j++)
                sm += fabs(A[i][j]);

        if (not(sm)) return -1; 

        if (counter < 3)
            thresh = 0.2 * sm / (n * n);
        else
            thresh = 0;

        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                double g = 100 * fabs(A[i][j]);
                if (counter > 3 && not(g))
                    A[i][j] = 0;

                else if (fabs(A[i][j]) > thresh) {
                    h = lambda[j] - lambda[i];
                    if (not(g))
                        t = (A[i][j]) / h;
                    else {
                        theta = 0.5 * h / A[i][j];
                        t = 1. / (fabs(theta) + sqrt(1 + theta * theta));
                        if (theta < 0) t = -t;
                    }
                    c = 1. / sqrt(1 + t * t);
                    s = t * c;
                    tau = s / (1 + c);
                    h = t * A[i][j];
                    z[i] -= h;
                    z[j] += h;
                    lambda[i] -= h;
                    lambda[j] += h;
                    A[i][j]=0;

                    for (int k = 0; k < i - 1; k++) 
                        rotate(A, k, i, k, j, g, s, tau, h);
                    for (int k = 0; k < j - 1; k++) 
                        rotate(A, i, k, k, j, g, s, tau, h);
                    for (int k = j; k < n; k++) 
                        rotate(A, i, k, j, k, g, s, tau, h);
                    for (int k = 0; k < n; k++) 
                        rotate(eigen_basis,k,i,k,j, g, s, tau, h);
                    n_rot++;
                }
            }
        }

        for (int i = 0; i < n; i++) {
            b[i] += z[i];
            lambda[i] = b[i];
            z[i] = 0.0;
        }
    } 
    return n_rot;
}
