#include <iostream>                                                   
#include <fstream>                                                    
#include <cmath>                                                      

using namespace std;

double pi (double, double, double);
double P (double, double, double, double);
double L (double, double, double);        
// double q (double, double);             
double media(double, double);             

int main() {
// tutte le unita' di misura sono centimetri!
        double p0 = 20.0;                    
        double dr = 0.270;                   
        double VV = 1.010;                   
        double F = 5.270;                    
        double n = 1.5168;                   
        double p1p2 = pi(VV,F,n);            

//      cout << p1p2 << endl;
        int max = 19;        
        int i;               
        for(i=0; i<max;i++) {
        double pl, ps1, ps2, ps;
        double p, l, q;
        double x,y;
        cin >> pl >> ps1 >> ps2;
//      cout << pl << " " << ps1 << " " << ps2 << endl;
        ps = media(ps1,ps2);
        p = P(pl, p0, dr, p1p2);
        l = L(ps,p0,p1p2);
        q =  l-p;
        x = 1./p;
        y = 1./q;
//      ostream elab;
//      elab.open("output",ios::out);
        cout << x << " " << y << " " << endl;
        }
        return 0;
}

double media(double x, double y) {
        return (x+y)/2.;
}

double pi (double vv, double f, double n) {
        return vv*(1-(4*f)/(4*n*f+vv));
        }

double P (double pl, double p0, double dr, double pp) {
        return pl - p0 + dr/2. - pp/2.;
        }

double L (double ps, double p0, double pp){
        return ps - p0 - pp;
        }

double q (double L, double p) {
        return L-p;
        }

