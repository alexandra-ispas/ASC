/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include "helper.h"
#include <stdlib.h>
#include <string.h>
#include <cblas.h>

/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	/* helper matrices */
	double *D = NULL;

	double *E = (double *) calloc(N * N, sizeof(double));
	DIE(E == NULL, "Allocation error.\n");

	/* create a copy of the 'B' matrix */
	matrix_copy (B, &D, N);

	/* D = B x A*/
	cblas_dtrmm(CblasRowMajor,
		CblasRight, /* to compute the multiplication in reverse order */
		CblasUpper, /* the secind matrix is upper triangular */
		CblasNoTrans,
		CblasNonUnit, N, N, 1.0,
		A, N, D, N
	);

	
	/* E = D x At */
	cblas_dgemm(
		CblasRowMajor,
		CblasNoTrans,
		CblasTrans,		/* use the transpose of the second matrix */
		N, N, N, 1.0,
		D, N, A, N, 0.0,
		E, /* store the result inside the 'E' matrix */
		N
	);


	/* E += B' x B */
	cblas_dgemm(
		CblasRowMajor,
		CblasTrans, /* use the transpose of the first matrix */
		CblasNoTrans,
		N, N, N, 1.0,
		B, /* the first matrix */
		N,
		B, /* the second matrix */
		N, 1.0,
		E, /* where to add the result */
		N
	);
	/* free unnecessary memory */
	free(D);

	return E;
}