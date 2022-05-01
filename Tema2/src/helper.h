#ifndef _HELPER_H
#define _HELPER_H

#define DIE(assertion, call_description)	\
	do {									\
		if (assertion) {					\
			fprintf(stderr, "(%s, %d): ",	\
					__FILE__, __LINE__);	\
			perror(call_description);		\
			exit(EXIT_FAILURE);				\
		}									\
	} while(0)

void matrix_copy (double *A, double **A_2, int N);

void matrix_multiply (double *A, unsigned char A_is_transp, unsigned char A_upper,
                    double *B, unsigned char B_is_transp, unsigned char B_upper,
                    double **C, int N);
#endif