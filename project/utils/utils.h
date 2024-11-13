#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

struct parsed_request {
    // the size of the key
    uint32_t matrices_size;
    // First matrix
    uint32_t *mat1;
    // Second matrix
    uint32_t *mat2;
    // The number of patterns
    uint32_t nb_patterns;
    // The size of the patterns
    uint32_t patterns_size;
    // The patterns to match
    uint32_t *patterns;
};


// Functions you are asked to implement

/**
 * @brief Parses a raw request into a nice struct
 *
 * @param request: A big string containing the request as it is received by the server
 * @param request_len: The size of the raw request
 * @param parsed : A struct that will contain the parsed request at the end of the function
 *
 * @note The variable `parsed` should be modified to store the parsed representation of the request.
 * @note `mat1`, `mat2` and `patterns` should point to the body of `request` at the location of each
 * element.
 */
void parse_request(struct parsed_request *parsed, char *request, size_t request_len);

/**
     * @brief Computes the product of two matrixes
     *
     * @param matrix1: a K x K matrix
     * @param matrix2: a K x K matrix
     * @param result: a K x K matrix that should contain the product of matrix1
     * and matrix2 at the end of the function
     * @param K: the size of the matrix
     *
     * @note `result` should be modified to the result of the multiplication of the matrices
 */
void multiply_matrix(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K);

/**
 * @brief Computes a measure of similarity between the patterns and the matrix
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
void test_patterns(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res);

/**
 * @brief Converts an array of uint32_t to a comma separated string of the numbers
 *
 * @param str: The string used to store the response
 * @param res: The array to transform into a string
 * @param res_size: The length of the the array `res`
 */
void res_to_string(char *str, uint32_t *res, uint32_t res_size);
