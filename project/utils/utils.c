#include "utils.h"

#include <stdint.h>
#include <stdio.h>
#include <string.h>

// Dummy function
int foo(void) { return 42; }

/**
 * @brief Parses a raw request into a nice struct
 *
 * @param request: A big string containing the request as it is received by the server
 * @param request_len: The size of the raw request
 * @param parsed : A struct that will contain the parsed request at the end of the function
 *
 * @note The variable `parsed` should be modified to store the parsed representation of the request.
 * @note `mat1`, `mat2` and `patterns` should point to the body of `request` at the location of each element.
*/
void parse_request(struct parsed_request *parsed, char *request, size_t request_len) {
    char buffer[50];
    int buf_index = 0;
    int comma_count = 0;
    int mat_size = 0;
    int cut_size = 0;
//    int matrix_index = 0;
//    int pattern_index = 0;

    for (size_t i = 0; i < request_len; i++) {
        if (request[i] == ',' || i == request_len-1) {
            // time to put request in parsed
            if (i == request_len - 1 && request[i] != ',') {
                buffer[buf_index++] = request[i];
            }
            buffer[buf_index] = '\0';  // for strtol to work

            // first ,
            if (comma_count == 0) {
                parsed->matrices_size = (uint32_t) strtol(buffer, NULL, 10);
                mat_size = parsed->matrices_size;
                cut_size = mat_size*mat_size*4;
            }
            // second ,
            else if (comma_count == 1) {
                parsed->nb_patterns = (uint32_t) strtol(buffer, NULL, 10);
            }
            // third ,
            else if (comma_count == 2) {
                parsed->patterns_size = (uint32_t) strtol(buffer, NULL, 10);
            }
            else if (comma_count >= 3) {
                // using comma_count as a counter from now on bcs why not
                for (int j = 0; (j < cut_size) && (i + j < request_len); j++) {
                    // mat1
                    if (comma_count == 3) {
                        char* substring = request;
                        strncpy(substring, buffer+(i+j), cut_size);
                        parsed->mat1 = (uint32_t *)substring;
                    }
                    // mat2
                    else if (comma_count == 4) {
                        char* substring = request;
                        strncpy(substring, buffer+(i+j), cut_size);
                        parsed->mat2 = (uint32_t *)substring;
                    }
                    // patterns
                    else if (comma_count == 5) {
                        char* substring = request;
                        strncpy(substring, buffer+(i+j), cut_size);
                        parsed->patterns = (uint32_t *)substring;
                    }
                }
                i += cut_size - 1;
            }

            // reset buffer
            buf_index = 0;
            comma_count++;
        }
        else {
            // expand buffer
            buffer[buf_index++] = request[i];
        }
    }
}

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
void multiply_matrix(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
    // initialize KxK matrix
    for(uint32_t i = 0; i < K; i++) {
        for(uint32_t j = 0; j < K; j++) {
            result[i*K + j] = 0;
        }
    }
    // fill matrix
    for(uint32_t i = 0; i < K; i++) {
        for(uint32_t j = 0; j < K; j++) {
            for (uint32_t k = 0; k < K; k++) {
                result[i*K + j] += matrix1[i*K + k] * matrix2[k*K + j];
            }
        }
    }
}

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
void test_patterns(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res) {
    (void)matrix;
    (void)matrix_size;
    (void)patterns;
    (void)pattern_size;
    (void)nb_patterns;
    (void)res;
    printf("CHANGE ME\n");
}

/**
 * @brief Converts an array of uint32_t to a comma separated string of the numbers
 *
 * @param str: The string used to store the response
 * @param res: The array to transform into a string
 * @param res_size: The length of the the array `res`
*/
void res_to_string(char *str, uint32_t *res, uint32_t res_size) {
    str[0] = '\0'; // otherwise it writes sh*t in the start
    for (uint32_t i = 0; i < res_size; i++) {
        char buffer[12];
        // number => string_number
        sprintf(buffer, "%u", res[i]);
        // string_number => str
        strcat(str, buffer);
        // if not last => comma
        if (i < res_size - 1) {
            strcat(str, ",");
        }
    }
}


//int main() {
//    uint32_t res_size = 3;
//    uint32_t res[] = {15, 16, 17};
//    char* string;
//    for (int i = 0; i < res_size; i++) {
//        printf("%d ", res[i]);
//    }
//    res_to_string(string, res, res_size);
//    printf("\n%s", string);
//    return 0;
//}
