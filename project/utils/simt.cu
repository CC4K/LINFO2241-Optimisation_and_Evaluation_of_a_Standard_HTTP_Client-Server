/*
    This file is compiled only if the flag SIMT is given
*/

/* By default, nvcc compiles with C++ linkage, but we want C linkage */
extern "C" {

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

#include "simt.h"

#ifndef CUDA_BLOCK_SIZE
    #define CUDA_BLOCK_SIZE 8
#endif



/*
    GPU kernel performing a matrix multiplication
    __global__ specifies that it will execute on the device (= the GPU)
 */
//  CUDA MATRIX MULT: https://stackoverflow.com/questions/18815489/cuda-tiled-matrix-matrix-multiplication-with-shared-memory-and-matrix-size-whic
 __global__ void kernel_multiply_matrix(uint32_t *A, uint32_t *B, uint32_t *C, uint32_t K) {

    uint32_t CValue = 0;
    
    int Row = blockIdx.y*blockDim.y + threadIdx.y;
    int Col = blockIdx.x*blockDim.y + threadIdx.x;

    __shared__ uint32_t As[CUDA_BLOCK_SIZE][CUDA_BLOCK_SIZE];
    __shared__ uint32_t Bs[CUDA_BLOCK_SIZE][CUDA_BLOCK_SIZE];


    for (int k = 0; k < (CUDA_BLOCK_SIZE + K - 1)/CUDA_BLOCK_SIZE; k++) {

            if (k*CUDA_BLOCK_SIZE + threadIdx.x < K && Row < K)
                As[threadIdx.y][threadIdx.x] = A[Row*K + k*CUDA_BLOCK_SIZE + threadIdx.x];
            else
                As[threadIdx.y][threadIdx.x] = 0;

            if (k*CUDA_BLOCK_SIZE + threadIdx.y < K && Col < K)
                Bs[threadIdx.y][threadIdx.x] = B[(k*CUDA_BLOCK_SIZE + threadIdx.y)*K + Col];
            else
                Bs[threadIdx.y][threadIdx.x] = 0;

            __syncthreads(); //prevents race conditions for shared memory
            
            for (int n = 0; n < CUDA_BLOCK_SIZE; ++n)
            CValue += As[threadIdx.y][n] * Bs[n][threadIdx.x];
            
            __syncthreads();
    }
        
    if (Row < K && Col < K)
        C[((blockIdx.y * blockDim.y + threadIdx.y)*K) +
            (blockIdx.x * blockDim.x)+ threadIdx.x] = CValue;
            
}




__global__ void kernel_test_patterns(uint32_t *matrix, uint32_t m, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res) {

    uint32_t i = blockIdx.y * blockDim.y + threadIdx.y;
    uint32_t j = blockIdx.x * blockDim.x + threadIdx.x;
    
    
    if ( i < (m - pattern_size + 1) && j < nb_patterns) {
        uint32_t dist = 0;
        uint32_t new_j = j * pattern_size;

        uint32_t k;
        for (k = 0; k + 7 < pattern_size; k += 8) {
            dist += (matrix[i + k] - patterns[new_j + k]) * (matrix[i + k] - patterns[new_j + k]);
            dist += (matrix[i + k + 1] - patterns[new_j + k + 1]) * (matrix[i + k + 1] - patterns[new_j + k + 1]);
            dist += (matrix[i + k + 2] - patterns[new_j + k + 2]) * (matrix[i + k + 2] - patterns[new_j + k + 2]);
            dist += (matrix[i + k + 3] - patterns[new_j + k + 3]) * (matrix[i + k + 3] - patterns[new_j + k + 3]);
            dist += (matrix[i + k + 4] - patterns[new_j + k + 4]) * (matrix[i + k + 4] - patterns[new_j + k + 4]);
            dist += (matrix[i + k + 5] - patterns[new_j + k + 5]) * (matrix[i + k + 5] - patterns[new_j + k + 5]);
            dist += (matrix[i + k + 6] - patterns[new_j + k + 6]) * (matrix[i + k + 6] - patterns[new_j + k + 6]);
            dist += (matrix[i + k + 7] - patterns[new_j + k + 7]) * (matrix[i + k + 7] - patterns[new_j + k + 7]);
        }

        for (; k < pattern_size; k++) {
            dist += (matrix[i + k] - patterns[new_j + k]) * (matrix[i + k] - patterns[new_j + k]);
        }
        
        atomicMin(&res[j], dist);
    }
    
}



uint32_t *cuda_memory = nullptr;
size_t allocated_size = 0;

/*
    Helper function that allocates GPU memory, copies the data to the GPU, and launches the kernel 
    It will execute on the host (= the CPU)

    Two functions were merged into one to optimize performance
*/
void multiply_matrix_and_test_patterns_simt(uint32_t *matrix1, uint32_t *matrix2, uint32_t K, uint32_t *patterns, uint32_t pattern_size, uint32_t nb_patterns, uint32_t *res){
    uint32_t matrix_size_1D = K * K;
    
    uint32_t  *A_cuda, *B_cuda, *C_cuda, *patterns_cuda, *res_cuda;

    uint32_t size_to_allocate_matrix = 3 * matrix_size_1D;
    uint32_t size_to_allocate_patterns = matrix_size_1D + nb_patterns + nb_patterns * pattern_size;
    size_t required_size = max(size_to_allocate_matrix, size_to_allocate_patterns);

    // CudaMalloc is a big bottleneck so it's usage is minimized to the strict minimum
    if (required_size > allocated_size) {
        if (cuda_memory != nullptr) {
            cudaFree(cuda_memory);
        }
        cudaMalloc(&cuda_memory, required_size * sizeof(uint32_t));
        allocated_size = required_size;
    }

    A_cuda = cuda_memory + 2 * matrix_size_1D;
    B_cuda = cuda_memory + matrix_size_1D;
    C_cuda = cuda_memory;

    patterns_cuda = cuda_memory + matrix_size_1D;
    res_cuda = cuda_memory + matrix_size_1D + nb_patterns*pattern_size;

    /* Copy matrices A and B from host to device */
    cudaMemcpy(A_cuda, matrix1, K * K * sizeof(uint32_t), cudaMemcpyHostToDevice);
    cudaMemcpy(B_cuda, matrix2, K * K * sizeof(uint32_t), cudaMemcpyHostToDevice);
    
    /* Define the block and grid dimensions */
    dim3 threadsPerBlock(CUDA_BLOCK_SIZE, CUDA_BLOCK_SIZE); 
    dim3 numBlocks((K + threadsPerBlock.x - 1) / threadsPerBlock.x, (K + threadsPerBlock.y - 1) / threadsPerBlock.y);  
    
    /* Launch the kernel */
    kernel_multiply_matrix <<< numBlocks, threadsPerBlock >>> (A_cuda, B_cuda, C_cuda, K);

    /* Wait for the kernel to finish */
    cudaDeviceSynchronize();

    cudaMemcpy(patterns_cuda, patterns, nb_patterns * pattern_size * sizeof(uint32_t), cudaMemcpyHostToDevice);
    
    cudaMemset(res_cuda, UINT32_MAX, nb_patterns * sizeof(uint32_t));
    
    dim3 numBlocks_patterns((nb_patterns + threadsPerBlock.x - 1) / threadsPerBlock.x, ((matrix_size_1D - pattern_size + 1) + threadsPerBlock.y - 1) / threadsPerBlock.y); 
    
    // the matrix from the multiplication while keeping it on the GPU
    kernel_test_patterns<<<numBlocks_patterns, threadsPerBlock>>>(C_cuda, matrix_size_1D, patterns_cuda, pattern_size, nb_patterns, res_cuda);

    cudaMemcpy(res, res_cuda, nb_patterns * sizeof(uint32_t), cudaMemcpyDeviceToHost);

}

} /* extern "C" */
