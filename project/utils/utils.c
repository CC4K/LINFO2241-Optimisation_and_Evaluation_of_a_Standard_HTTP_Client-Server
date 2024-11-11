#include "utils.h"

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
    char *current = request;
    char *comma;

    // matrices_size
    parsed->matrices_size = strtol(current, &comma, 10);
    if (comma[0] == ',') {
        current = comma+1;
    }

    // nb_patterns
    parsed->nb_patterns = strtol(current, &comma, 10);
    if (comma[0] == ',') {
        current = comma+1;
    }

    // patterns_size
    parsed->patterns_size = strtol(current, &comma, 10);
    if (comma[0] == ',') {
        current = comma+1;
    }

    #ifdef DBEST
        uint32_t matrix_size_bytes = parsed->matrices_size * parsed->matrices_size * sizeof(uint32_t);
        // mat1
        parsed->mat1 = (uint32_t *) current;
        current += matrix_size_bytes;

        // mat2
        parsed->mat2 = (uint32_t *) current;
        current += matrix_size_bytes;
    #else
        // mat1
        parsed->mat1 = (uint32_t *) current;
        current += parsed->matrices_size*parsed->matrices_size*sizeof(uint32_t);

        // mat2
        parsed->mat2 = (uint32_t *) current;
        current += parsed->matrices_size*parsed->matrices_size*sizeof(uint32_t);
    #endif

    // patterns
    parsed->patterns = (uint32_t *) current;

    // idk really
    if (*current == (char) request_len) return;
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
    // initialize result
    for(uint32_t i = 0; i < K; i++) {
        for(uint32_t j = 0; j < K; j++) {
            result[i*K + j] = 0;
        }
    }
    // multiply mat1 & mat2
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
#if (defined(DCACHE_AWARE) && defined(DUNROLL)) || defined(DBEST)
            uint32_t k = 0;
            uint32_t sum = 0;
            for (; k <= K - 8; k += 8) {
                uint32_t mat1_0 = matrix1[i*K + k + 0];
                uint32_t mat1_1 = matrix1[i*K + k + 1];
                uint32_t mat1_2 = matrix1[i*K + k + 2];
                uint32_t mat1_3 = matrix1[i*K + k + 3];
                uint32_t mat1_4 = matrix1[i*K + k + 4];
                uint32_t mat1_5 = matrix1[i*K + k + 5];
                uint32_t mat1_6 = matrix1[i*K + k + 6];
                uint32_t mat1_7 = matrix1[i*K + k + 7];

                sum += mat1_0 * matrix2[j + (k+0)*K];
                sum += mat1_1 * matrix2[j + (k+1)*K];
                sum += mat1_2 * matrix2[j + (k+2)*K];
                sum += mat1_3 * matrix2[j + (k+3)*K];
                sum += mat1_4 * matrix2[j + (k+4)*K];
                sum += mat1_5 * matrix2[j + (k+5)*K];
                sum += mat1_6 * matrix2[j + (k+6)*K];
                sum += mat1_7 * matrix2[j + (k+7)*K];
            }
            for (; k < K; k++) {
                sum += matrix1[i*K + k + 0] * matrix2[j + (k+0)*K];
            }
            result[i*K + j] = sum;
#elif defined(DCACHE_AWARE) && !defined(DUNROLL)
            uint32_t mat1_ij = matrix1[i*K + j];
            for (uint32_t k = 0; k < K; k++) {
                result[i*K + k] += mat1_ij * matrix2[j*K + k];
            }
#endif
#if !defined(DCACHE_AWARE) && defined(DUNROLL)
            uint32_t k = 0;
            uint32_t sum = 0;
            for (; k <= K - 8; k += 8) {
                sum += matrix1[i*K + k + 0] * matrix2[j + (k+0)*K];
                sum += matrix1[i*K + k + 1] * matrix2[j + (k+1)*K];
                sum += matrix1[i*K + k + 2] * matrix2[j + (k+2)*K];
                sum += matrix1[i*K + k + 3] * matrix2[j + (k+3)*K];
                sum += matrix1[i*K + k + 4] * matrix2[j + (k+4)*K];
                sum += matrix1[i*K + k + 5] * matrix2[j + (k+5)*K];
                sum += matrix1[i*K + k + 6] * matrix2[j + (k+6)*K];
                sum += matrix1[i*K + k + 7] * matrix2[j + (k+7)*K];
            }
            for (; k < K; k++) {
                sum += matrix1[i*K + k + 0] * matrix2[j + (k+0)*K];
            }
            result[i*K + j] = sum;
#elif !defined(DCACHE_AWARE) && !defined(DUNROLL) && !defined(DBEST)
            for (uint32_t k = 0; k < K; k++) {
                result[i*K + j] += matrix1[i*K + k] * matrix2[k*K + j];
            }
#endif
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
    uint32_t n = nb_patterns; // 2
    uint32_t m = matrix_size*matrix_size; // 8*8 = 64

    for (uint32_t i = 0; i < n; i++) res[i] = UINT32_MAX;

    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) { // 0 => 64-16 + 1 = 48 + 1 = 49
        for (uint32_t j = 0; j < n; j++) { // 0 => 2
            uint32_t dist = 0;
            uint32_t new_j = j * pattern_size; // j * 16
#if defined(DUNROLL) || defined(DBEST)
            uint32_t k = 0;
            for (; k < pattern_size - 4; k += 4) { // 0 => 16
                dist += (matrix[i + k + 0] - patterns[new_j + k + 0])*(matrix[i + k + 0] - patterns[new_j + k + 0]);
                dist += (matrix[i + k + 1] - patterns[new_j + k + 1])*(matrix[i + k + 1] - patterns[new_j + k + 1]);
                dist += (matrix[i + k + 2] - patterns[new_j + k + 2])*(matrix[i + k + 2] - patterns[new_j + k + 2]);
                dist += (matrix[i + k + 3] - patterns[new_j + k + 3])*(matrix[i + k + 3] - patterns[new_j + k + 3]);
            }
            for (; k < pattern_size; k++) {
                dist += (matrix[i + k] - patterns[new_j + k])*(matrix[i + k] - patterns[new_j + k]);
            }
#else
            for (uint32_t k = 0; k < pattern_size; k++) { // 0 => 8
                dist += (matrix[i + k] - patterns[new_j + k])*(matrix[i + k] - patterns[new_j + k]);
            }
#endif
            //printf("j = %d\tdist = %d\n", j, dist); PQ CA FAIT TT BUGGER WTF
            uint32_t min = (dist < res[j]) ? dist : res[j];
            res[j] = min;
        }
    }
}

/**
 * @brief Converts an array of uint32_t to a comma separated string of the numbers
 *
 * @param str: The string used to store the response
 * @param res: The array to transform into a string
 * @param res_size: The length of the the array `res`
*/
void res_to_string(char *str, uint32_t *res, uint32_t res_size) {
    str[0] = '\0';
    char buffer[11]; 
    for (size_t i = 0; i < res_size; i++) {
        if (i == res_size - 1) {
            sprintf(buffer, "%d", res[i]);
            strcat(str, buffer);
            return;
        }
        sprintf(buffer, "%d,", res[i]);
        strcat(str, buffer);
    }

    // base code
    // str[0] = '\0'; // otherwise it writes sh*t in the start
    // for (uint32_t i = 0; i < res_size; i++) {
    //     char buffer[12];
    //     // number => string_number
    //     sprintf(buffer, "%u", res[i]);
    //     // string_number => str
    //     strcat(str, buffer);
    //     // if not last => comma
    //     if (i < res_size - 1) {
    //         strcat(str, ",");
    //     }
    // }
}
