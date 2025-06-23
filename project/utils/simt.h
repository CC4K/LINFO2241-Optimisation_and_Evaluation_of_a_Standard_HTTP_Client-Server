#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <cuda_runtime.h>

/**
 * @brief Computes the product of two matrixes, **by launching a CUDA kernel**
 *
 * @param matrix1: a K x K matrix
 * @param matrix2: a K x K matrix
 * @param result: a K x K matrix that should contain the product of matrix1
 * and matrix2 at the end of the function
 * @param K: the size of the matrix
 *
 * @note `result` should be modified to the result of the multiplication of the matrices
*/
// void multiply_matrix_simt(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K);
// void test_patterns_simt(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res);
void multiply_matrix_and_test_patterns_simt(uint32_t *matrix1, uint32_t *matrix2, uint32_t K, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res);
// TODO add other functions if you need it
