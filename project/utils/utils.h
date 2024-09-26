#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

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
void parse_request(struct parsed_request *parsed, char *request, size_t request_len);
void multiply_matrix(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K);
void test_patterns(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res);
void res_to_string(char *str, uint32_t *res, uint32_t res_size);
//char *complete_algorithm(char *raw_request, uint32_t raw_request_len, char *res_str, uint32_t *res_uint, uint32_t *intermediary_matrix, uint32_t *resp_len);