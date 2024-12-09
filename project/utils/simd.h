#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <immintrin.h>

/**
 * @brief Computes the product of two matrixes, **using SIMD instructions**
 *
 * @param matrix1: a K x K matrix
 * @param matrix2: a K x K matrix
 * @param result: a K x K matrix that should contain the product of matrix1
 * and matrix2 at the end of the function
 * @param K: the size of the matrix
 *
 * @note `result` should be modified to the result of the multiplication of the matrices
*/
void multiply_matrix_simd(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K);

/**
 * @brief Computes a measure of similarity between the patterns and the matrix, **using SIMD instructions**
 *
 * @param matrix: The matrix to search patterns in
 * @param matrix_size: The size of the matrix
 * @param patterns: The list of patterns
 * @param pattern_size: The size of each pattern
 * @param nb_patterns: The number of patterns
 * @param res: The result, the list of shortest distances for each pattern
 * @param K : The dimension of the file matrix
 *
 * @note `file` should be modified to contain the encrypted file.
 */
void test_patterns_simd(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res);
