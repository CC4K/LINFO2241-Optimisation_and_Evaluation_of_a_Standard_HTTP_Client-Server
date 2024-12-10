#include "simd.h"

//#define SIMD128
//#define SIMD256
//#define SIMD512

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
#if defined SIMD128
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n * sizeof(uint32_t));
    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t *matrix_ptr = &matrix[i]; // pointer to current matrix start
            uint32_t *pattern_ptr = &patterns[j * pattern_size]; // pointer to current pattern start

            __m128i vdist = _mm_setzero_si128();  // init squared diff acc
            uint32_t k = 0;
            for (; k + 3 < pattern_size; k += 4) {
                __m128i vmat = _mm_loadu_si128((__m128i*)(matrix_ptr + k));
                __m128i vpat = _mm_loadu_si128((__m128i*)(pattern_ptr + k));

                __m128i vdiff = _mm_sub_epi32(vmat, vpat); // matrix - patterns
                __m128i vsq = _mm_mullo_epi32(vdiff, vdiff); // (matrix - patterns)^2
                vdist = _mm_add_epi32(vdist, vsq); // squared diff
            }
            uint32_t temp[4];
            _mm_storeu_si128((__m128i*)temp, vdist);
            for (int x = 0; x < 4; x++) {
                dist += temp[x];
            }
            // rest just in case
            for (; k < pattern_size; k++) {
                uint32_t diff = *(matrix_ptr + k) - *(pattern_ptr + k);
                dist += diff * diff;
            }
            // update min dist
            res[j] = (dist < res[j]) ? dist : res[j];
        }
    }
#elif defined SIMD256 || defined SIMDBEST
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n * sizeof(uint32_t));
    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t *matrix_ptr = &matrix[i]; // pointer to current matrix start
            uint32_t *pattern_ptr = &patterns[j * pattern_size]; // pointer to current pattern start

            __m256i vdist = _mm256_setzero_si256();  // init squared diff acc
            uint32_t k = 0;
            for (; k + 7 < pattern_size; k += 8) {
                __m256i vmat = _mm256_loadu_si256((__m256i*)(matrix_ptr + k));
                __m256i vpat = _mm256_loadu_si256((__m256i*)(pattern_ptr + k));

                __m256i vdiff = _mm256_sub_epi32(vmat, vpat); // matrix - patterns
                __m256i vsq = _mm256_mullo_epi32(vdiff, vdiff); // (matrix - patterns)^2
                vdist = _mm256_add_epi32(vdist, vsq); // squared diff
            }
            uint32_t temp[8];
            _mm256_storeu_si256((__m256i*)temp, vdist);
            for (int x = 0; x < 8; x++) {
                dist += temp[x];
            }
            // rest just in case
            for (; k < pattern_size; k++) {
                uint32_t diff = *(matrix_ptr + k) - *(pattern_ptr + k);
                dist += diff * diff;
            }
            // update min dist
            res[j] = (dist < res[j]) ? dist : res[j];
        }
    }
#elif defined SIMD512
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n * sizeof(uint32_t));
    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t *matrix_ptr = &matrix[i]; // pointer to current matrix start
            uint32_t *pattern_ptr = &patterns[j * pattern_size]; // pointer to current pattern start

            __m512i vdist = _mm512_setzero_si512();  // init squared diff acc
            uint32_t k = 0;
            for (; k + 15 < pattern_size; k += 16) {
                __m512i vmat = _mm512_loadu_si512((__m512i*)(matrix_ptr + k));
                __m512i vpat = _mm512_loadu_si512((__m512i*)(pattern_ptr + k));

                __m512i vdiff = _mm512_sub_epi32(vmat, vpat); // matrix - patterns
                __m512i vsq = _mm512_mullo_epi32(vdiff, vdiff); // (matrix - patterns)^2
                vdist = _mm512_add_epi32(vdist, vsq); // squared diff
            }
            uint32_t temp[16];
            _mm512_storeu_si512((__m512i*)temp, vdist);
            for (int x = 0; x < 16; x++) {
                dist += temp[x];
            }
            // rest just in case
            for (; k < pattern_size; k++) {
                uint32_t diff = *(matrix_ptr + k) - *(pattern_ptr + k);
                dist += diff * diff;
            }
            // update min dist
            res[j] = (dist < res[j]) ? dist : res[j];
        }
    }
#else
#error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
#endif
}


//int main() {
//    // "run" with CLion to activate code correction
//    return 0;
//}
