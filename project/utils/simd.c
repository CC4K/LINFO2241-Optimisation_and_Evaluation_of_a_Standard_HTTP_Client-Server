#include "simd.h"

//#define SIMD128
#define SIMD256
//#define SIMD512

// make -B run_release_simd CFLAGS+="-DSIMDBEST"

void multiply_matrix_simd(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
    (void)matrix1;
    (void)matrix2;
    (void)result;
    (void)K;

#if defined SIMD128
    // Use SSE
    #error SIMD128 Not implemented
#elif defined SIMD256
    // Use AVX2
    // TODO: 256 first then super EZ PZ
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
            for (uint32_t k = 0; k < K; k++) {
                result[i * K + j] += matrix1[i * K + k] * matrix2[k * K + j];
            }
        }
    }


#elif defined SIMD512 || defined SIMDBEST
    // Use AVX512
    #error SIMD512 Not implemented
#else
#error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
#endif

    return;
}


void test_patterns_simd(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res) {
    (void)matrix;
    (void)matrix_size;
    (void)patterns;
    (void)patterns;
    (void)pattern_size;
    (void)nb_patterns;
    (void)res;

#if defined SIMD128
// Use SSE
#error SIMD128 Not implemented
#elif defined SIMD256
    // Use AVX2
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n*sizeof(uint32_t));

    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t new_j = j * pattern_size;
            for (uint32_t k = 0; k < pattern_size; k++) {
                dist += (matrix[i + k] - patterns[new_j + k])*(matrix[i + k] - patterns[new_j + k]);
            }
            uint32_t min = (dist < res[j]) ? dist : res[j];
            res[j] = min;
        }
    }


#elif defined SIMD512 || defined SIMDBEST
// Use AVX512
#error SIMD512 Not implemented
#else
#error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
#endif

    return;
}



//int main() {
//    // "run" with CLion to activate code correction
//    return 0;
//}
