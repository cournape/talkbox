#ifndef _TALKBOX_LEVINSON_C_
#define _TALKBOX_LEVINSON_C_

int levinson(const double* in, int order, double* acoeff, double* err,
             double* kcoeff, double* tmp);

#endif
