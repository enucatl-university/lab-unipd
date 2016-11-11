from ROOT import TMath
from math import sqrt, pi, exp, log

def normal_inv(p):
    a = (-3.969683028665376e+01,  2.209460984245205e+02, \
            -2.759285104469687e+02,  1.383577518672690e+02, \
            -3.066479806614716e+01,  2.506628277459239e+00)
    b = (-5.447609879822406e+01,  1.615858368580409e+02, \
            -1.556989798598866e+02,  6.680131188771972e+01, \
            -1.328068155288572e+01 )
    c = (-7.784894002430293e-03, -3.223964580411365e-01, \
            -2.400758277161838e+00, -2.549732539343734e+00, \
            4.374664141464968e+00,  2.938163982698783e+00)
    d = (7.784695709041462e-03,  3.224671290700398e-01, \
            2.445134137142996e+00,  3.754408661907416e+00)

    if p >= 1.0 or p < 0.0:
        raise ValueError( "Argument to inverse normal cumulative function %f must be in open interval (0,1)" %p)

    if p == 0:
        return 0
    q = min(p, 1 - p)

    if q > 0.02425: 
    #/* Rational approximation for central region. */
        u = q - 0.5
        t = u*u
        u = u*(((((a[0]*t+a[1])*t+a[2])*t+a[3])*t+a[4])*t+a[5])\
                /(((((b[0]*t+b[1])*t+b[2])*t+b[3])*t+b[4])*t+1)

    else:
#/* Rational approximation for tail region. */
        t = sqrt(-2*log(q))
        u = (((((c[0]*t+c[1])*t+c[2])*t+c[3])*t+c[4])*t+c[5])\
        /((((d[0]*t+d[1])*t+d[2])*t+d[3])*t+1)
#     /* The relative error of the approximation has absolute value less
#than 1.15e-9.  One iteration of Halley's rational method (third
#order) gives full machine precision... */
    t = 0.5 * TMath.Erfc(-u / sqrt(2)) - q  #  /* error */
    t = t * sqrt(2 * pi) * exp(u * u / 2)  # /* f(u)/df(u) */
    u = u - t / (1 + u * t / 2)    # /* Halley's method */

    if p > 0.5:
        return -u
    else:
        return u

def kolm_to_sigma(kolm_prob): 
    #especially designed for my kolmogorov tests
    return abs(normal_inv(kolm_prob / 2))
