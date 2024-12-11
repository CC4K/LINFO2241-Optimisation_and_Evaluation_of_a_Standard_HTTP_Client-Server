#include "simd.h"

//#define SIMD128
//#define SIMD256
//#define SIMD512


void multiply_matrix_simd(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
#if defined SIMD128
    for (uint32_t i = 0; i < K; i++) {
        uint32_t k = 0;
        uint32_t j = 0;
        uint32_t i_K = i*K;
        for (; j < K; j++) {
            uint32_t mat1_ij = matrix1[i_K + j];
            __m128i mat1_ij_vec = _mm_set1_epi32(mat1_ij);
            // pointers
            uint32_t *result_ptr = result + i_K;
            uint32_t *mat2_ptr = matrix2 + j * K;
            k = 0;
            for (; k + 3 < K; k += 4) {
                __m128i mat2_vec = _mm_loadu_si128((__m128i *)(mat2_ptr + k));
                __m128i result_vec = _mm_loadu_si128((__m128i *)(result_ptr + k));
                // multiplication
                __m128i prod_vec = _mm_mullo_epi32(mat1_ij_vec, mat2_vec);
                // addition
                result_vec = _mm_add_epi32(result_vec, prod_vec);
                // store to result matrix
                _mm_storeu_si128((__m128i *)(result_ptr + k), result_vec);
            }
            // continue just in case larger than 4
            for (; k < K; k++) {
                result_ptr[k] += mat1_ij * mat2_ptr[k];
            }
        }
    }
#elif defined SIMD256 || defined SIMDBEST
    for (uint32_t i = 0; i < K; i++) {
        uint32_t k = 0;
        uint32_t j = 0;
        uint32_t i_K = i*K;
        for (; j < K; j++) {
            uint32_t mat1_ij = matrix1[i_K + j];
            __m256i mat1_ij_vec = _mm256_set1_epi32(mat1_ij);
            // pointers
            uint32_t *result_ptr = result + i_K;
            uint32_t *mat2_ptr = matrix2 + j * K;
            k = 0;
            for (; k + 7 < K; k += 8) {
                __m256i mat2_vec = _mm256_loadu_si256((__m256i *)(mat2_ptr + k));
                __m256i result_vec = _mm256_loadu_si256((__m256i *)(result_ptr + k));
                // multiplication
                __m256i prod_vec = _mm256_mullo_epi32(mat1_ij_vec, mat2_vec);
                // addition
                result_vec = _mm256_add_epi32(result_vec, prod_vec);
                // store to result matrix
                _mm256_storeu_si256((__m256i *)(result_ptr + k), result_vec);
            }
            // continue just in case larger than 8
            for (; k < K; k++) {
                result_ptr[k] += mat1_ij * mat2_ptr[k];
            }
        }
    }
#elif defined SIMD512
    for (uint32_t i = 0; i < K; i++) {
        uint32_t k = 0;
        uint32_t j = 0;
        uint32_t i_K = i*K;
        for (; j < K; j++) {
            uint32_t mat1_ij = matrix1[i_K + j];
            __m512i mat1_ij_vec = _mm512_set1_epi32(mat1_ij);
            // pointers
            uint32_t *result_ptr = result + i_K;
            uint32_t *mat2_ptr = matrix2 + j * K;
            k = 0;
            for (; k + 15 < K; k += 16) {
                __m512i mat2_vec = _mm512_loadu_si512((__m512i *)(mat2_ptr + k));
                __m512i result_vec = _mm512_loadu_si512((__m512i *)(result_ptr + k));
                // multiplication
                __m512i prod_vec = _mm512_mullo_epi32(mat1_ij_vec, mat2_vec);
                // addition
                result_vec = _mm512_add_epi32(result_vec, prod_vec);
                // store to result matrix
                _mm512_storeu_si512((__m512i *)(result_ptr + k), result_vec);
            }
            // continue just in case larger than 16
            for (; k < K; k++) {
                result_ptr[k] += mat1_ij * mat2_ptr[k];
            }
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
            uint32_t k = 0;
            uint32_t new_j = j * pattern_size;

            // pointers for matrix and patterns
            uint32_t *matrix_ptr = matrix + i;
            uint32_t *pattern_ptr = patterns + new_j;
            // storage
            __m128i v_dist = _mm_setzero_si128();
            for (; k + 3 < pattern_size; k += 4) {
                __m128i v_matrix = _mm_loadu_si128((__m128i*)matrix_ptr);
                __m128i v_pattern = _mm_loadu_si128((__m128i*)pattern_ptr);

                __m128i v_diff = _mm_sub_epi32(v_matrix, v_pattern); // (matrix - pattern)
                __m128i v_sq_diff = _mm_mullo_epi32(v_diff, v_diff); // (matrix - pattern)^2
                v_dist = _mm_add_epi32(v_dist, v_sq_diff); // squared diff

                matrix_ptr += 4;
                pattern_ptr += 4;
            }
            // horizontal sum in v_dist
            v_dist = _mm_hadd_epi32(v_dist, v_dist);
            v_dist = _mm_hadd_epi32(v_dist, v_dist);
            dist += _mm_cvtsi128_si32(v_dist);
            // continue just in case larger than 4
            for (; k < pattern_size; k++) {
                uint32_t diff = *matrix_ptr++ - *pattern_ptr++;
                dist += diff * diff;
            }
            // update min dist
            if (dist < res[j]) res[j] = dist;
        }
    }
#elif defined SIMD256 || defined SIMDBEST
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n * sizeof(uint32_t));
    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t k = 0;
            uint32_t new_j = j * pattern_size;

            // pointers for matrix and patterns
            uint32_t *matrix_ptr = matrix + i;
            uint32_t *pattern_ptr = patterns + new_j;
            // storage
            __m256i v_dist = _mm256_setzero_si256();
            for (; k + 7 < pattern_size; k += 8) {
                __m256i v_matrix = _mm256_loadu_si256((__m256i*)matrix_ptr);
                __m256i v_pattern = _mm256_loadu_si256((__m256i*)pattern_ptr);

                __m256i v_diff = _mm256_sub_epi32(v_matrix, v_pattern); // (matrix - pattern)
                __m256i v_sq_diff = _mm256_mullo_epi32(v_diff, v_diff); // (matrix - pattern)^2
                v_dist = _mm256_add_epi32(v_dist, v_sq_diff); // squared diff

                matrix_ptr += 8;
                pattern_ptr += 8;
            }
            // horizontal sum in v_dist
            __m128i v_low = _mm256_castsi256_si128(v_dist);
            __m128i v_high = _mm256_extracti128_si256(v_dist, 1);
            __m128i v_sum = _mm_add_epi32(v_low, v_high);
            v_sum = _mm_hadd_epi32(v_sum, v_sum);
            v_sum = _mm_hadd_epi32(v_sum, v_sum);
            dist += _mm_cvtsi128_si32(v_sum);
            // continue just in case larger than 8
            for (; k < pattern_size; k++) {
                uint32_t diff = *matrix_ptr++ - *pattern_ptr++;
                dist += diff * diff;
            }
            // update min dist
            if (dist < res[j]) res[j] = dist;
        }
    }
#elif defined SIMD512
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n * sizeof(uint32_t));
    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t k = 0;
            uint32_t new_j = j * pattern_size;

            // pointers for matrix and patterns
            uint32_t *matrix_ptr = matrix + i;
            uint32_t *pattern_ptr = patterns + new_j;
            // storage
            __m512i v_dist = _mm512_setzero_si512();
            for (; k + 15 < pattern_size; k += 16) {
                __m512i v_matrix = _mm512_loadu_si512((__m512i*)matrix_ptr);
                __m512i v_pattern = _mm512_loadu_si512((__m512i*)pattern_ptr);

                __m512i v_diff = _mm512_sub_epi32(v_matrix, v_pattern); // (matrix - pattern)
                __m512i v_sq_diff = _mm512_mullo_epi32(v_diff, v_diff); // (matrix - pattern)^2
                v_dist = _mm512_add_epi32(v_dist, v_sq_diff); // squared diff

                matrix_ptr += 16;
                pattern_ptr += 16;
            }
            // horizontal sum in v_dist
            //dist += _mm512_reduce_add_epi32(v_dist);
            uint32_t temp[16];
            _mm512_storeu_si512((__m512i*)temp, v_dist);
            for (int x = 0; x < 16; x++) {
                dist += temp[x];
            }
            // continue just in case larger than 16
            for (; k < pattern_size; k++) {
                uint32_t diff = *matrix_ptr++ - *pattern_ptr++;
                dist += diff * diff;
            }
            // update min dist
            if (dist < res[j]) res[j] = dist;
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
