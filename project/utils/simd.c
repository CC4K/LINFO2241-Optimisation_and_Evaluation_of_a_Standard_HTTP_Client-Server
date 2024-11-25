/*
    This file is compiled only if the flag SIMD is given
*/

#include "simd.h"

void multiply_matrix_simd(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
    (void)matrix1;
    (void)matrix2;
    (void)result;
    (void)K;

    // TODO multiply the matrices using SSE, AVX/AVX2 or AVX512, using the directives SIMD128, SIMD256 and SIMD512.
    // TODO the SIMDBEST flag should give the version with the best performance.
    // TODO for example, if you think the AVX512 version is the best, you could do:
#if defined SIMD128
    // Use SSE
    #error SIMD128 Not implemented
#elif defined SIMD256
    // Use AVX2
    #error SIMD256 Not implemented
#elif defined SIMD512 || defined SIMDBEST   // TODO is this the best version? 
    // Use AVX512
    #error SIMD512 Not implemented
#else
#error "Please define either SIMD128, SIMD256, SIMD512 or SIMDBEST. If you see this message at compilation, you forget a -D flag."
#endif

    return;
}

// TODO add other functions if you need it