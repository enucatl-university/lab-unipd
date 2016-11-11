// =====================================================================================
// 
//       Filename:  silvestrelli.cpp
// 
//    Description:  fatto da silvestrelli
// 
//        Version:  1.0
//        Created:  16/11/2009 11:31:43
//       Revision:  none
//       Compiler:  g++
// 
//         Author:  Matteo Abis (), matteo@latinblog.org
//        Company:  
// 
// =====================================================================================

                                         /* 
************************************************************************
*  rk4.c: 4th order Runge-Kutta solution for harmonic oscillator       *
*								       *
************************************************************************
*/
       
#include <iostream>
#include <cmath>
#include <fstream>

#define N 2                                   // number of equations 
#define MIN 0.0                               // minimum x 
#define MAX 10.0                              // maximum x 

int main()
{
   using namespace std;
   double dist, e0, etot, detot, x, y[N];
   int j;
   
   void runge4(double x, double y[], double step);
   double f(double x, double y[], int i);
   
   ofstream out;
   out.open ("rk4.out");                      // save data in rk4.dat

   cout << " stepsize ?" << endl;            // read stepsize 
   cin >> dist;

   e0 = 0.5;                                  // initial exact energy 
   
   y[0] = 1.0;                                // initial position  
   y[1] = 0.0;                                // initial velocity  

   detot = 0.0; 
   
   for(x = MIN; x <= MAX ; x += dist)
   {
      runge4(x, y, dist);
      etot=0.5*(y[0]*y[0]+y[1]*y[1]);         // total energy 
      detot=etot-e0;
      out << x+dist<< " " << y[0] << " " << cos(x+dist) << " " << detot << endl;
   }
   cout << "data stored in rk4.out" << endl;
}
/*-----------------------end of main program--------------------------*/

/* Runge-Kutta subroutine */
void runge4(double x, double y[], double step)
{
   double f(double x, double y[], int i);
   double h=step/2.0,                         // the midpoint 
          t1[N], t2[N], t3[N],                // temporary storage 
          k1[N], k2[N], k3[N],k4[N];          // for Runge-Kutta  
   int i;
 
   for (i=0; i<N; i++) t1[i] = y[i]+0.5*(k1[i]=step*f(x, y, i));
   for (i=0; i<N; i++) t2[i] = y[i]+0.5*(k2[i]=step*f(x+h, t1, i));
   for (i=0; i<N; i++) t3[i] = y[i]+    (k3[i]=step*f(x+h, t2, i));
   for (i=0; i<N; i++) k4[i] =                 step*f(x + step, t3, i);
      
   for (i=0; i<N; i++) y[i] += (k1[i]+2*k2[i]+2*k3[i]+k4[i])/6.0;
}
//--------------------------------------------------------------------

// definition of equations - this is the harmonic oscillator 
double  f(double x, double y[], int i)
{
   if (i == 0) return(y[1]);               // RHS of first equation 
   if (i == 1) return(-y[0]);              // RHS of second equation 
}

