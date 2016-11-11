#ifndef  JACOBI2_INC
#define  JACOBI2_INC

#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>
#include <iterator>

typedef std::vector<double> vec;
typedef std::vector< std::vector<double> > mat;

// =====================================================================================
//        Class:  Jacobi
//  Description:  l
// =====================================================================================
class Jacobi
{
    public:

        // ====================  LIFECYCLE     =======================================
        Jacobi(mat& S);                             // constructor

        // ====================  ACCESSORS     =======================================
        void get_eigensystem(vec& e, mat& E);
        int get_n_rot() const { return n_rot; }

        // ====================  MUTATORS      =======================================
        int max_ind(int k);
        int pivot_ind();
        void update(int k, double t);
        void rotate(int k, int l, int i, int j);

        // ====================  OPERATORS     =======================================

        // ====================  DATA MEMBERS  =======================================
    protected:

    private:
        mat S, E;
        vec e;
        double s, c, p, y;
        int n, state, n_rot;
        std::vector<int> ind, changed;

}; // -----  end of class Jacobi  -----

bool abs_compare(double x, double y);
#endif // ----- #ifndef JACOBI2_INC  -----
