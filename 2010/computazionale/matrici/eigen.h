#ifndef  EIGEN_INC
#define  EIGEN_INC
// =====================================================================================
// 
//       Filename:  jacobi.cpp
// 
//    Description:  Calcola tutti gli AUTOVALORI e gli AUTOVETTORI di una matrice      
//                  REALE, SIMMETRICA col metodo di Jacobi:                            
//                  in "ouput" gli elementi della matrice 'A' sopra la diagonale sono  
//                  distrutti, il vettore 'd' contiene gli autovalori e la matrice 'eigen_basis' 
//                  ha, come colonne, gli autovettori normalizzati; 'nrot' registra il 
//                  numero di rotazioni di Jacobi necessarie.                          
// 
//        Created:  22/11/2009 11:43:24
//       Compiler:  g++
// 
//         Author:  Giorgio Bettineschi
// 
// =====================================================================================

#include <iostream>
#include <cmath>
#include <vector>

typedef std::vector<double> vec;
typedef std::vector< std::vector<double> > mat;


int jacobi(mat& A, vec& lambda, mat& eigen_basis);

inline void rotate(mat& A, int i, int j, int k, int l, double g, double s, double tau, double h){
    g = A[i][j];
    h = A[k][l];
    A[i][j] = g - s * (h + g * tau);
    A[k][l] = h + s * (g - h * tau);
}

#endif // ----- #ifndef EIGEN_INC  -----
