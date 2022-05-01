#include "helper.h"
#include <stdio.h>
#include <stdlib.h>

void matrix_copy (double *A, double **A_2, int N) {
    int matrix_size = N * N, i = 0;

    /* allocate memory for the auxiliary matrix */
	*A_2 = (double *) calloc(matrix_size, sizeof(double));
	DIE(*A_2 == NULL, "Allocation error.\n");

    for (; i < matrix_size; i++) {
        (*A_2)[i] = A[i];
    }
}

void matrix_multiply (double *A, unsigned char A_is_transp, unsigned char A_upper,
                    double *B, unsigned char B_is_transp, unsigned char B_upper,
                    double **C, int N) {
    int i, j, k, k1, k2;
    for (i = 0; i < N; i++)
		for (j = 0; j < N; j++) {
            if (A_upper) {
                k1 = j;
                k2 = N - 1;
            } else if (B_upper) {
                k1 = 0;
                k2 = j;
            } else {
                k1 = 0;
                k2 = N - 1;
            }
			for (k = k1; k <= k2; k++) {
                if (A_is_transp) {
                    (*C)[i * N + j] += A[k * N + i] * B[k * N + j];
                } else if (B_is_transp) {
                    (*C)[i * N + j] += A[i * N + k] * B[j * N + k];
                } else {
                    (*C)[i * N + j] += A[i * N + k] * B[k * N + j];
                }
            }
        }
}
