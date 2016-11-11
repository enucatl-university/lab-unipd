#ifndef  GAUSS_INC
#define  GAUSS_INC
#include <cmath>
#include <vector>

typedef std::vector<double> vec;
typedef std::vector< std::vector<double> > mat;

void gauss(mat A, vec b, vec& x);
void lu_decomposition(mat& A, mat& L, mat& U);
void lu_solve(mat& A, vec& b, vec& x);
double det_upper(mat& U);
void invert(mat& A, mat& I);
#endif // ----- #ifndef GAUSS_INC  -----
