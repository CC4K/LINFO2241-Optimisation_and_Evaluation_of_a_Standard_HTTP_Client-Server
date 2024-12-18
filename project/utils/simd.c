#include "simd.h"

//#define SIMD128
//#define SIMD256
//#define SIMD512

void multiply_matrix_simd(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
    for (uint32_t i = 0; i < K; i++) {
        uint32_t j = 0;
        uint32_t k = 0;
        uint32_t iK = i*K;
        for (; j < K; j++) {
            uint32_t mat1_iK_j = matrix1[iK + j];
            // pointers for result and matrix2
            uint32_t *result_iK_ptr = result + iK;
            uint32_t *mat2_jK_ptr = matrix2 + j*K;
            k = 0;
            #if defined SIMD128
            __m128i v_mat1_iK_j = _mm_set1_epi32(mat1_iK_j);
            for (; k + 3 < K; k += 4) {
                __m128i v_mat2 = _mm_loadu_si128((__m128i *)(mat2_jK_ptr + k));
                __m128i v_result = _mm_loadu_si128((__m128i *)(result_iK_ptr + k));
                // multiplication
                __m128i v_prod = _mm_mullo_epi32(v_mat1_iK_j, v_mat2);
                // addition
                v_result = _mm_add_epi32(v_result, v_prod);
                // store to result matrix
                _mm_storeu_si128((__m128i *)(result_iK_ptr + k), v_result);
            }
            #elif defined SIMD256
            __m256i v_mat1_iK_j = _mm256_set1_epi32(mat1_iK_j);
            for (; k + 7 < K; k += 8) {
                __m256i v_mat2 = _mm256_loadu_si256((__m256i *)(mat2_jK_ptr + k));
                __m256i v_result = _mm256_loadu_si256((__m256i *)(result_iK_ptr + k));
                // multiplication
                __m256i v_prod = _mm256_mullo_epi32(v_mat1_iK_j, v_mat2);
                // addition
                v_result = _mm256_add_epi32(v_result, v_prod);
                // store to result matrix
                _mm256_storeu_si256((__m256i *)(result_iK_ptr + k), v_result);
            }
            #elif defined SIMD512 || defined SIMDBEST
            __m512i v_mat1_iK_j = _mm512_set1_epi32(mat1_iK_j);
            for (; k + 15 < K; k += 16) {
                __m512i v_mat2 = _mm512_loadu_si512((__m512i *)(mat2_jK_ptr + k));
                __m512i v_result = _mm512_loadu_si512((__m512i *)(result_iK_ptr + k));
                // multiplication
                __m512i v_prod = _mm512_mullo_epi32(v_mat1_iK_j, v_mat2);
                // addition
                v_result = _mm512_add_epi32(v_result, v_prod);
                // store to result matrix
                _mm512_storeu_si512((__m512i *)(result_iK_ptr + k), v_result);
            }
            #else
            #error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
            #endif
            // continue just in case larger
            for (; k < K; k++) {
                result_iK_ptr[k] += mat1_iK_j * mat2_jK_ptr[k];
            }
        }
    }
}


void test_patterns_simd(uint32_t *matrix, uint32_t matrix_size, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res) {
    uint32_t n = nb_patterns;
    uint32_t m = matrix_size * matrix_size;
    memset(res, UINT32_MAX, n * sizeof(uint32_t));
    
    for (uint32_t i = 0; i < (m - pattern_size + 1); i++) {
        for (uint32_t j = 0; j < n; j++) {
            uint32_t dist = 0;
            uint32_t k = 0;
            uint32_t new_j = j * pattern_size;
            // pointers for matrix and patterns
            uint32_t *matrix_i_ptr = matrix + i;
            uint32_t *pattern_new_j_ptr = patterns + new_j;
            #if defined SIMD128
            // storage
            __m128i v_dist = _mm_setzero_si128();
            for (; k + 3 < pattern_size; k += 4) {
                __m128i v_matrix = _mm_loadu_si128((__m128i*)matrix_i_ptr);
                __m128i v_pattern = _mm_loadu_si128((__m128i*)pattern_new_j_ptr);

                __m128i v_diff = _mm_sub_epi32(v_matrix, v_pattern); // (matrix - pattern)
                __m128i v_sq_diff = _mm_mullo_epi32(v_diff, v_diff); // (matrix - pattern)^2
                v_dist = _mm_add_epi32(v_dist, v_sq_diff); // squared diff

                matrix_i_ptr += 4;
                pattern_new_j_ptr += 4;
            }
            // horizontal sum in v_dist
            v_dist = _mm_hadd_epi32(v_dist, v_dist);
            v_dist = _mm_hadd_epi32(v_dist, v_dist);
            dist += _mm_cvtsi128_si32(v_dist);
            #elif defined SIMD256
            // storage
            __m256i v_dist = _mm256_setzero_si256();
            for (; k + 7 < pattern_size; k += 8) {
                __m256i v_matrix = _mm256_loadu_si256((__m256i*)matrix_i_ptr);
                __m256i v_pattern = _mm256_loadu_si256((__m256i*)pattern_new_j_ptr);

                __m256i v_diff = _mm256_sub_epi32(v_matrix, v_pattern); // (matrix - pattern)
                __m256i v_sq_diff = _mm256_mullo_epi32(v_diff, v_diff); // (matrix - pattern)^2
                v_dist = _mm256_add_epi32(v_dist, v_sq_diff); // squared diff

                matrix_i_ptr += 8;
                pattern_new_j_ptr += 8;
            }
            // horizontal sum in v_dist
            __m128i v_low = _mm256_castsi256_si128(v_dist);
            __m128i v_high = _mm256_extracti128_si256(v_dist, 1);
            __m128i v_sum = _mm_add_epi32(v_low, v_high);
            v_sum = _mm_hadd_epi32(v_sum, v_sum);
            v_sum = _mm_hadd_epi32(v_sum, v_sum);
            dist += _mm_cvtsi128_si32(v_sum);
            #elif defined SIMD512 || defined SIMDBEST
            // storage
            __m512i v_dist = _mm512_setzero_si512();
            for (; k + 15 < pattern_size; k += 16) {
                __m512i v_matrix = _mm512_loadu_si512((__m512i*)matrix_i_ptr);
                __m512i v_pattern = _mm512_loadu_si512((__m512i*)pattern_new_j_ptr);

                __m512i v_diff = _mm512_sub_epi32(v_matrix, v_pattern); // (matrix - pattern)
                __m512i v_sq_diff = _mm512_mullo_epi32(v_diff, v_diff); // (matrix - pattern)^2
                v_dist = _mm512_add_epi32(v_dist, v_sq_diff); // squared diff

                matrix_i_ptr += 16;
                pattern_new_j_ptr += 16;
            }
            // horizontal sum in v_dist
            dist += _mm512_reduce_add_epi32(v_dist);
            #else
            #error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
            #endif
            // continue just in case larger
            for (; k < pattern_size; k++) {
                uint32_t diff = *matrix_i_ptr++ - *pattern_new_j_ptr++;
                dist += diff * diff;
            }
            // update min dist
            if (dist < res[j]) res[j] = dist;
        }
    }
}
