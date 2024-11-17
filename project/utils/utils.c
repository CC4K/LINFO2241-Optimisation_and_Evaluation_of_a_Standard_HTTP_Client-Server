#include "utils.h"

//#define UNROLL
//#define CACHE_AWARE
//#define BEST

void parse_request(struct parsed_request *parsed, char *request, size_t request_len) {
    char *current = request;
    char *comma;

    // matrices_size
    parsed->matrices_size = strtol(current, &comma, 10);
    if (comma[0] == ',') {
        current = comma + 1;
    }
    // nb_patterns
    parsed->nb_patterns = strtol(current, &comma, 10);
    if (comma[0] == ',') {
        current = comma + 1;
    }
    // patterns_size
    parsed->patterns_size = strtol(current, &comma, 10);
    if (comma[0] == ',') {
        current = comma + 1;
    }

#ifdef BEST
    uint32_t matrix_size_bytes = parsed->matrices_size * parsed->matrices_size * sizeof(uint32_t);

    // mat1
    parsed->mat1 = (uint32_t *)current;
    current += matrix_size_bytes;
    // mat2
    parsed->mat2 = (uint32_t *)current;
    current += matrix_size_bytes;
    // patterns
    parsed->patterns = (uint32_t *)current;

    if (*current == (char)request_len) return;
#else
    // mat1
    parsed->mat1 = (uint32_t *)current;
    current += parsed->matrices_size * parsed->matrices_size * sizeof(uint32_t);
    // mat2
    parsed->mat2 = (uint32_t *)current;
    current += parsed->matrices_size * parsed->matrices_size * sizeof(uint32_t);
    // patterns
    parsed->patterns = (uint32_t *)current;

    if (*current == (char)request_len) return;
#endif
}

#ifdef BEST

#define UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j, k) \
    k=0;\
    for (; k + 7 < K; k += 8) { \
        result[i * K + k] += mat1_ij * matrix2[j * K + k]; \
        result[i * K + k + 1] += mat1_ij * matrix2[j * K + k + 1]; \
        result[i * K + k + 2] += mat1_ij * matrix2[j * K + k + 2]; \
        result[i * K + k + 3] += mat1_ij * matrix2[j * K + k + 3]; \
        result[i * K + k + 4] += mat1_ij * matrix2[j * K + k + 4]; \
        result[i * K + k + 5] += mat1_ij * matrix2[j * K + k + 5]; \
        result[i * K + k + 6] += mat1_ij * matrix2[j * K + k + 6]; \
        result[i * K + k + 7] += mat1_ij * matrix2[j * K + k + 7]; \
    } \
    for (; k < K; k++) { \
        result[i * K + k] += mat1_ij * matrix2[j * K + k]; \
    }


void multiply_matrix(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
    for (uint32_t i = 0; i < K; i++) {
        uint32_t k = 0;
        uint32_t j = 0;
        // for (; j +7< K; j+=8) {
        //     uint32_t mat1_ij = matrix1[i * K + j];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j, k);
        //     mat1_ij = matrix1[i * K + j+1];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j+1, k);
        //     mat1_ij = matrix1[i * K + j+2];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j+2, k);
        //     mat1_ij = matrix1[i * K + j+3];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j+3, k);
        //     mat1_ij = matrix1[i * K + j+4];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j+4, k);
        //     mat1_ij = matrix1[i * K + j+5];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j+5, k);
        //     mat1_ij = matrix1[i * K + j+6];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j+6, k);
        //     mat1_ij = matrix1[i * K + j+7];
        //     UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j+7, k);
        // }
        uint32_t i_K = i*K;
        for (; j < K; j++) {
            uint32_t mat1_ij = matrix1[i_K+ j];
            UNROLL_LOOP_8(result, i, K, mat1_ij, matrix2, j, k);
        }
    }
}


__always_inline void test_patterns(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res) {
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n*sizeof(uint32_t));

    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t new_j = j * pattern_size;
            uint32_t k = 0;
            for (; k + 7 < pattern_size; k += 8) {
                dist += (matrix[i + k + 0] - patterns[new_j + k + 0]) * (matrix[i + k + 0] - patterns[new_j + k + 0]);
                dist += (matrix[i + k + 1] - patterns[new_j + k + 1]) * (matrix[i + k + 1] - patterns[new_j + k + 1]);
                dist += (matrix[i + k + 2] - patterns[new_j + k + 2]) * (matrix[i + k + 2] - patterns[new_j + k + 2]);
                dist += (matrix[i + k + 3] - patterns[new_j + k + 3]) * (matrix[i + k + 3] - patterns[new_j + k + 3]);
                dist += (matrix[i + k + 4] - patterns[new_j + k + 4]) * (matrix[i + k + 4] - patterns[new_j + k + 4]);
                dist += (matrix[i + k + 5] - patterns[new_j + k + 5]) * (matrix[i + k + 5] - patterns[new_j + k + 5]);
                dist += (matrix[i + k + 6] - patterns[new_j + k + 6]) * (matrix[i + k + 6] - patterns[new_j + k + 6]);
                dist += (matrix[i + k + 7] - patterns[new_j + k + 7]) * (matrix[i + k + 7] - patterns[new_j + k + 7]);
            }
            for (; __builtin_expect(k < pattern_size,0); k++) {
                dist += (matrix[i + k] - patterns[new_j + k]) * (matrix[i + k] - patterns[new_j + k]);
            }
            if(dist < res[j]){
                res[j] = dist;
            }
        }
    }
}

#else

void multiply_matrix(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
            #if defined(CACHE_AWARE)
            uint32_t mat1_ij = matrix1[i * K + j];
            for (uint32_t k = 0; k < K; k++) {
                result[i * K + k] += mat1_ij * matrix2[j * K + k];
            }
            #elif defined(UNROLL)
            uint32_t k = 0;
            uint32_t sum = 0;
            for (; k + 7 < K; k += 8) {
                sum += matrix1[i * K + k + 0] * matrix2[j + (k + 0) * K];
                sum += matrix1[i * K + k + 1] * matrix2[j + (k + 1) * K];
                sum += matrix1[i * K + k + 2] * matrix2[j + (k + 2) * K];
                sum += matrix1[i * K + k + 3] * matrix2[j + (k + 3) * K];
                sum += matrix1[i * K + k + 4] * matrix2[j + (k + 4) * K];
                sum += matrix1[i * K + k + 5] * matrix2[j + (k + 5) * K];
                sum += matrix1[i * K + k + 6] * matrix2[j + (k + 6) * K];
                sum += matrix1[i * K + k + 7] * matrix2[j + (k + 7) * K];
            }
            for (; k + 3 < K; k += 4) {
                sum += matrix1[i * K + k + 0] * matrix2[j + (k + 0) * K];
                sum += matrix1[i * K + k + 1] * matrix2[j + (k + 1) * K];
                sum += matrix1[i * K + k + 2] * matrix2[j + (k + 2) * K];
                sum += matrix1[i * K + k + 3] * matrix2[j + (k + 3) * K];
            }
            for (; k < K; k++) {
                sum += matrix1[i * K + k + 0] * matrix2[j + (k + 0) * K];
            }
            result[i * K + j] = sum;
            #else
            for (uint32_t k = 0; k < K; k++) {
                result[i * K + j] += matrix1[i * K + k] * matrix2[k * K + j];
            }
            #endif
        }
    }
}

void test_patterns(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res) {
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n*sizeof(uint32_t));

    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t new_j = j * pattern_size;
            #if defined(UNROLL)
            uint32_t k = 0;
            for (; k + 7 < pattern_size; k += 8) {
                dist += (matrix[i + k + 0] - patterns[new_j + k + 0]) *(matrix[i + k + 0] - patterns[new_j + k + 0]);
                dist += (matrix[i + k + 1] - patterns[new_j + k + 1]) *(matrix[i + k + 1] - patterns[new_j + k + 1]);
                dist += (matrix[i + k + 2] - patterns[new_j + k + 2]) *(matrix[i + k + 2] - patterns[new_j + k + 2]);
                dist += (matrix[i + k + 3] - patterns[new_j + k + 3]) *(matrix[i + k + 3] - patterns[new_j + k + 3]);
                dist += (matrix[i + k + 4] - patterns[new_j + k + 4]) *(matrix[i + k + 4] - patterns[new_j + k + 4]);
                dist += (matrix[i + k + 5] - patterns[new_j + k + 5]) *(matrix[i + k + 5] - patterns[new_j + k + 5]);
                dist += (matrix[i + k + 6] - patterns[new_j + k + 6]) *(matrix[i + k + 6] - patterns[new_j + k + 6]);
                dist += (matrix[i + k + 7] - patterns[new_j + k + 7]) *(matrix[i + k + 7] - patterns[new_j + k + 7]);
            }
            for (; k + 3 < pattern_size; k += 4) {
                dist += (matrix[i + k + 0] - patterns[new_j + k + 0]) *(matrix[i + k + 0] - patterns[new_j + k + 0]);
                dist += (matrix[i + k + 1] - patterns[new_j + k + 1]) *(matrix[i + k + 1] - patterns[new_j + k + 1]);
                dist += (matrix[i + k + 2] - patterns[new_j + k + 2]) *(matrix[i + k + 2] - patterns[new_j + k + 2]);
                dist += (matrix[i + k + 3] - patterns[new_j + k + 3]) *(matrix[i + k + 3] - patterns[new_j + k + 3]);
            }
            for (; k < pattern_size; k++) {
                dist += (matrix[i + k] - patterns[new_j + k]) * (matrix[i + k] - patterns[new_j + k]);
            }
            #else
            for (uint32_t k = 0; k < pattern_size; k++) {
                dist += (matrix[i + k] - patterns[new_j + k]) * (matrix[i + k] - patterns[new_j + k]);
            }
            #endif
            uint32_t min = (dist < res[j]) ? dist : res[j];
            res[j] = min;
        }
    }
}
#endif


void res_to_string(char *str, uint32_t *res, uint32_t res_size) {
    str[0] = '\0';
    char buffer[11];

#if defined(BEST)
    for (size_t i = 0; i < res_size - 1; i++) {
        sprintf(buffer, "%d,", res[i]);
        strcat(str, buffer);
    }
    sprintf(buffer, "%d", res[res_size - 1]);
    strcat(str, buffer);
    return;

#else
    for (size_t i = 0; i < res_size; i++) {
        if (i == res_size - 1) {
            sprintf(buffer, "%d", res[i]);
            strcat(str, buffer);
            return;
        }
        sprintf(buffer, "%d,", res[i]);
        strcat(str, buffer);
    }
#endif
}
