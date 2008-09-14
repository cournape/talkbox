/*
 * Last Change: Mon Sep 08 11:00 PM 2008 J
 */
#include <float.h>
#include <math.h> /* for isfinite */
#include <stdio.h>

#include "levinson.h"

/*
 * The actual computation :
 *      - in    : the input vector which defines the toeplitz matrix
 *      - size  : size of in (ie number of elements)
 *      - order : size of the system to solve. order must be < size -1
 *      - acoeff: solution (ie ar coefficients). Size must be at last order+1
 *      - err   : *prediction* error (scalar)
 *      - kcoeff: reflexion coefficients. Size must be at last equal to equal to order.
 *      - tmp   : cache, mnust have at least order elements
 *
 * this function assume all arrays are allocated with the right size, and that
 * the parameters make sense. No checking is done, must be done before calling
 * this function: in particular, in[0] must be non zero.
 *
 * Returns 0 on success, -1 if a compuation error happened (overflow, underflow
 * for error calculation)
 */

int levinson(const double* in, int order, double* acoeff, double* err,
             double* kcoeff, double* tmp)
{
        int i, j;
        double  acc;
        int ret = 0;

        /* order 0 */
        acoeff[0] = (double)1.0;
        *err = in[0];

        /* order >= 1 */
        for (i = 1; i <= order; ++i) {
                acc = in[i];
                for ( j = 1; j <= i-1; ++j) {
                        acc += acoeff[j]*in[i-j];
                }
                kcoeff[i-1] = -acc/(*err);
                acoeff[i] = kcoeff[i-1];

                for (j = 0; j < order; ++j) {
                        tmp[j] = acoeff[j];
                }

                for (j = 1; j < i; ++j) {
                        acoeff[j] += kcoeff[i-1]*tmp[i-j];
                }
                *err *= (1-kcoeff[i-1]*kcoeff[i-1]);
        }

        return ret;
}
