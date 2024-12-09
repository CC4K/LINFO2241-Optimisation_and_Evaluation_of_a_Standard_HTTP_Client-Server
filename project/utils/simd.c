#include "simd.h"

//#define SIMD128
#define SIMD256
//#define SIMD512

// make -B run_release_simd CFLAGS+="-DSIMDBEST"

void multiply_matrix_simd(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
#if defined SIMD128
    // Use SSE
    #error SIMD128 Not implemented
#elif defined SIMD256
    // Use AVX2
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
            __m256i sum_vec = _mm256_setzero_si256();
            uint32_t k = 0;
            for (; k + 7 < K; k += 8) {
                // load 8 elements from matrix1 row and matrix2 column
                __m256i vec1 = _mm256_loadu_si256((__m256i*)&matrix1[i * K + k]);
                __m256i vec2 = _mm256_set_epi32(
                    matrix2[j + (k + 7) * K], matrix2[j + (k + 6) * K],
                    matrix2[j + (k + 5) * K], matrix2[j + (k + 4) * K],
                    matrix2[j + (k + 3) * K], matrix2[j + (k + 2) * K],
                    matrix2[j + (k + 1) * K], matrix2[j + k * K]);
                // multiply and accumulate
                __m256i prod = _mm256_mullo_epi32(vec1, vec2);
                sum_vec = _mm256_add_epi32(sum_vec, prod);
            }
            uint32_t sum = 0;
            uint32_t temp[8];
            _mm256_storeu_si256((__m256i*)temp, sum_vec);
            for (int x = 0; x < 8; x++) {
                sum += temp[x];
            }
            // rest
            for (; k < K; k++) {
                sum += matrix1[i * K + k] * matrix2[j + k * K];
            }
            result[i * K + j] = sum;
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
