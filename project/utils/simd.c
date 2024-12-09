#include "simd.h"

//#define SIMD128
#define SIMD256
//#define SIMD512

// make -B run_release_simd CFLAGS+="-DSIMDBEST"

void multiply_matrix_simd(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
#if defined SIMD128
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
            __m128i sum_vec = _mm_setzero_si128();
            uint32_t *row_ptr = matrix1 + i * K; // pointer to current row of matrix1
            uint32_t *col_ptr = matrix2 + j; // pointer to 1st element of matrix2 column
            uint32_t k = 0;
            for (; k + 3 < K; k += 4) {
                // load 4 elements from matrix1 row
                __m128i vec1 = _mm_loadu_si128((__m128i*)row_ptr);
                // move pointer forward
                row_ptr += 4;
                // load 4 elements from matrix2 column
                __m128i vec2 = _mm_set_epi32(
                    col_ptr[(k + 3) * K], col_ptr[(k + 2) * K],
                    col_ptr[(k + 1) * K], col_ptr[k * K]);
                // multiply and accumulate
                __m128i prod = _mm_mullo_epi32(vec1, vec2);
                sum_vec = _mm_add_epi32(sum_vec, prod);
            }
            uint32_t sum = 0;
            uint32_t temp[4];
            _mm_storeu_si128((__m128i*)temp, sum_vec);
            for (int x = 0; x < 4; x++) {
                sum += temp[x];
            }
            // rest just in case
            for (; k < K; k++) {
                sum += row_ptr[0] * col_ptr[k * K];
                row_ptr++;
            }
            result[i * K + j] = sum;
        }
    }
#elif defined SIMD256 || defined SIMDBEST
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
            __m256i sum_vec = _mm256_setzero_si256();
            uint32_t *row_ptr = matrix1 + i * K; // pointer to current row of matrix1
            uint32_t *col_ptr = matrix2 + j; // pointer to 1st element of matrix2 column
            uint32_t k = 0;
            for (; k + 7 < K; k += 8) {
                // load 8 elements from matrix1 row
                __m256i vec1 = _mm256_loadu_si256((__m256i*)row_ptr);
                // move pointer forward
                row_ptr += 8;
                // load 8 elements from matrix2 column
                __m256i vec2 = _mm256_set_epi32(
                    col_ptr[(k + 7) * K], col_ptr[(k + 6) * K],
                    col_ptr[(k + 5) * K], col_ptr[(k + 4) * K],
                    col_ptr[(k + 3) * K], col_ptr[(k + 2) * K],
                    col_ptr[(k + 1) * K], col_ptr[k * K]);
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
            // rest just in case
            for (; k < K; k++) {
                sum += row_ptr[0] * col_ptr[k * K];
                row_ptr++;
            }
            result[i * K + j] = sum;
        }
    }
#elif defined SIMD512
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
            __m512i sum_vec = _mm512_setzero_si512();
            uint32_t *row_ptr = matrix1 + i * K; // pointer to current row of matrix1
            uint32_t *col_ptr = matrix2 + j; // pointer to 1st element of matrix2 column
            uint32_t k = 0;
            for (; k + 15 < K; k += 16) {
                // load 16 elements from matrix1 row
                __m512i vec1 = _mm512_loadu_si512((__m512i *)row_ptr);
                // move pointer forward
                row_ptr += 16;
                // load 16 elements from matrix2 column
                __m512i vec2 = _mm512_set_epi32(
                    col_ptr[(k + 15) * K], col_ptr[(k + 14) * K],
                    col_ptr[(k + 13) * K], col_ptr[(k + 12) * K],
                    col_ptr[(k + 11) * K], col_ptr[(k + 10) * K],
                    col_ptr[(k + 9) * K],  col_ptr[(k + 8) * K],
                    col_ptr[(k + 7) * K],  col_ptr[(k + 6) * K],
                    col_ptr[(k + 5) * K],  col_ptr[(k + 4) * K],
                    col_ptr[(k + 3) * K],  col_ptr[(k + 2) * K],
                    col_ptr[(k + 1) * K],  col_ptr[k * K]);
                // multiply and accumulate
                __m512i prod = _mm512_mullo_epi32(vec1, vec2);
                sum_vec = _mm512_add_epi32(sum_vec, prod);
            }
            uint32_t sum = 0;
            uint32_t temp[16];
            _mm512_storeu_si512((__m512i *)temp, sum_vec);
            for (int x = 0; x < 16; x++) {
                sum += temp[x];
            }
            // rest just in case
            for (; k < K; k++) {
                sum += row_ptr[0] * col_ptr[k * K];
                row_ptr++;
            }
            result[i * K + j] = sum;
        }
    }
#else
#error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
#endif
}


void test_patterns_simd(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res) {
    (void)matrix;
    (void)matrix_size;
    (void)patterns;
    (void)patterns;
    (void)pattern_size;
    (void)nb_patterns;
    (void)res;

//#if defined SIMD128
//// Use SSE
//#elif defined SIMD256
//    // Use AVX2
//    uint32_t n = nb_patterns;
//    uint32_t m = matrix_size * matrix_size;
//    memset(res, UINT32_MAX, n*sizeof(uint32_t));
//
//    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
//        for (uint32_t j = 0; j < n; j++) {
//            uint32_t dist = 0;
//            uint32_t new_j = j * pattern_size;
//            for (uint32_t k = 0; k < pattern_size; k++) {
//                dist += (matrix[i + k] - patterns[new_j + k])*(matrix[i + k] - patterns[new_j + k]);
//            }
//            uint32_t min = (dist < res[j]) ? dist : res[j];
//            res[j] = min;
//        }
//    }
//#elif defined SIMD512 || defined SIMDBEST
//// Use AVX512
//#error SIMD512 Not implemented
//#else
//#error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
//#endif

    return;
}



//int main() {
//    // "run" with CLion to activate code correction
//    return 0;
//}
