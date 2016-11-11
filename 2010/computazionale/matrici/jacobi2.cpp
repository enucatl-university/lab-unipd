#include "jacobi2.h"

using namespace std;
Jacobi::Jacobi(mat& S_){
    n_rot = 0;
    S = S_;
    n = S.size();
    e.resize(n, 0);
    E.resize(n, vec(n, 0));
    ind.resize(n, 0);
    changed.resize(n, 1);

    //initialize E to identity,
    //e to diagonal
    //max_ind array
    for (int i = 0; i < n; i++){
        E[i][i] = 1;
        e[i] = S[i][i];
        ind[i] = max_ind(i);
    }
    state = n;

    while (state){ //next rotation

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            std::cout << S[i][j] << " ";
        }
        std::cout << std::endl;
    }

        //find index of pivot;
        int k = pivot_ind();
        int l = ind[k];
        p = S[k][l];
        cout << "pivot " << k << " " << l << " " << p << endl;

        if (not(fabs(p))) break;
        y = 0.5 * (e[l] - e[k]);
        double t = fabs(y) + sqrt(p * p + y * y);
        s = sqrt(p * p + t * t);
        c = t / s;
        s = p / s;
        t = p * p / t;

        if (y < 0){
            s = -s;
            t = -t;
        }

        S[k][l] = 0;
        update(k, -t);
        update(l, t);

        for (int i = 0; i < k - 1; i++) rotate(i, k, i, l);
        for (int i = k; i < l - 1; i++) rotate(k, i, i, l);
        for (int i = l + 1; i < n; i++) rotate(k, i, l, i);
        for (int i = 0; i < n; i++){
            double temp = E[k][i];
            E[k][i] = c * temp - s * E[l][i];
            E[l][i] = s * temp + c * E[l][i];
        }

        //k and l rows have changed!
        ind[k] = max_ind(k);
        ind[l] = max_ind(l);
        n_rot++;
    }
}

int Jacobi::max_ind(int k){
    int el = static_cast<int>(std::distance(
                S[k].begin(),
                std::max_element(S[k].begin() + k + 1, S[k].end(), abs_compare)));
    return el;
}

int Jacobi::pivot_ind(){
    vec temp(n, 0);
    for (int i = 0; i < n - 1; i++) temp[i] = S[i][ind[i]];
    int el = static_cast<int>(std::distance(
                temp.begin(),
                std::max_element(temp.begin(), temp.end(), abs_compare)));
    return el;
}

void Jacobi::update(int k, double t){
    y = e[k];
    e[k] = y + t;
    if (changed[k] and y == e[k]){
        changed[k] = 0;
        state--;
    }
    else if (not(changed[k]) and y != e[k]){
        changed[k] = 1;
        state++;
    }
}

void Jacobi::rotate(int k, int l, int i, int j){
    double temp = S[k][l];
    S[k][l] = c * temp - s * S[i][j];
    S[i][j] = s * temp + c * S[i][j];
}

void Jacobi::get_eigensystem(vec& e_, mat& E_){
    e_ = e;
    E_ = E;
}

bool abs_compare(double x, double y){
    return fabs(x) < fabs(y);
}
