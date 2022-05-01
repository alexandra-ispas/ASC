/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "helper.h"
#include "utils.h"

/*
 * Add your unoptimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	int matrix_size = N * N;

	/* allocate memory for the auxiliary matrices */
	double *D = (double *) calloc(matrix_size, sizeof(double));
	DIE(D == NULL, "Allocation error.\n");

	double *E = (double *) calloc(matrix_size, sizeof(double));
	DIE(E == NULL, "Allocation error.\n");
	
	/* D = B x A */
	matrix_multiply(B, 0, 0, A, 0, 1, &D, N);

	/* E = D * A' */
	matrix_multiply(D, 0, 1, A, 1, 0, &E, N);

	/* E += B' x B */
	matrix_multiply(B, 1, 0, B, 0, 0, &E, N);
	
	/* free unncessary matrix */
	free(D);

	return E;
}
