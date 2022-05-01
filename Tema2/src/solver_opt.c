/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include "helper.h"

/*
 * Add your optimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	int i = 0, j, k;

	/* allocate memory for the auxiliary matrices */
	double *D = (double *) calloc(N * N, sizeof(double));
	DIE(D == NULL, "Allocation error.\n");

	double *E = (double *) calloc(N * N, sizeof(double));
	DIE(E == NULL, "Allocation error.\n");

	register double *b_line_i = NULL;
	register double *d_line_i = NULL;
	register double *e_line_i = NULL;
	register double sum;
	
	/* D = B x A */
	for (; i < N; i++) {
		b_line_i = B + i * N;
		d_line_i = D + i * N;
		for (j = 0; j < N; j++) {
			sum = 0;
			register double *a_col_j = A + j;
			register double *b_aux = b_line_i;
			for (k = 0; k <= j; k++) {
				sum += *b_aux * *(a_col_j);
				a_col_j += N;
				b_aux++;
			}
			*(d_line_i++) = sum;
		}
	}

	/* E = D * A' */
	for (i = 0; i < N; i++) {
		d_line_i = D + i * N;
		e_line_i = E + i * N;
		for (j = 0; j < N; j++) {
			register double *a_line_j = A + j * N + j;
			sum = 0;
			register double *d_line_i_col_k = d_line_i + j;
			for (k = j; k < N; k++) {
				sum += *d_line_i_col_k * *a_line_j;
				a_line_j++;
				d_line_i_col_k++; 
			}
			*(e_line_i++) = sum;
		}
	}

	/* E += B' x B */
	for (i = 0; i < N; i++) {
		e_line_i = E + i * N;
		for (j = 0; j < N; ++j) {
			sum = *(e_line_i);
			register double *b_col_j = B + j;
			register double *b_col_i = B + i;
			k = 0;
			while (k < N) {
				sum += *b_col_i * *b_col_j;
				b_col_i += N;
				b_col_j += N;
				k++;
			}
			*(e_line_i++) = sum;
		}
	}
	
	/* free unncessary matrix */
	free(D);

	return E;
}
