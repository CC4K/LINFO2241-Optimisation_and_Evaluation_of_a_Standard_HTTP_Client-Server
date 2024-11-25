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
#define CUDA_BLOCK_SIZE 16  // TODO change this value to the best you found during your analysis
#endif

/*
    GPU kernel performing a matrix multiplication
    __global__ specifies that it will execute on the device (= the GPU)
 */
__global__ void kernel_multiply_matrix(uint32_t *A, uint32_t *B, uint32_t *C, uint32_t K) {

    // TODO write the kernel code
    // Here you can use blockIdx, blockDim and threadIdx
    uint32_t row = blockIdx.y * blockDim.y + threadIdx.y;
    uint32_t col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < K && col < K) {
        // TODO we want a multiplication!
        C[row * K + col] = A[row * K + col] + B[row * K + col];
        
        #error SIMT Not implemented
    }
}


/*
    Helper function that allocates GPU memory, copies the data to the GPU, amd launches the kernel 
    It will execute on the host (= the CPU)
    Feel free to modify it!
*/
void multiply_matrix_simt(uint32_t *matrix1, uint32_t *matrix2, uint32_t *result, uint32_t K) {
    /* Allocate GPU memory for the matrices */
    uint32_t *A_d, *B_d, *C_d;
    cudaMalloc(&A_d, K * K * sizeof(uint32_t));
    cudaMalloc(&B_d, K * K * sizeof(uint32_t));
    cudaMalloc(&C_d, K * K * sizeof(uint32_t));

    /* Copy matrices A and B from host to device */
    cudaMemcpy(A_d, matrix1, K * K * sizeof(uint32_t), cudaMemcpyHostToDevice);
    cudaMemcpy(B_d, matrix2, K * K * sizeof(uint32_t), cudaMemcpyHostToDevice);

    /* Define the block and grid dimensions */
    // TODO what block size do you want?
    dim3 threadsPerBlock(CUDA_BLOCK_SIZE, CUDA_BLOCK_SIZE); // e.g., 16x16 threads per block
    dim3 numBlocks((K + threadsPerBlock.x - 1) / threadsPerBlock.x, (K + threadsPerBlock.y - 1) / threadsPerBlock.y);   // try to understand why such computations!
    
    /* Launch the kernel */
    kernel_multiply_matrix <<< numBlocks, threadsPerBlock >>> (A_d, B_d, C_d, K);

    /* Wait for the kernel to finish */
    cudaDeviceSynchronize();

    /* Copy the result matrix C from device to host */
    cudaMemcpy(result, C_d, K * K * sizeof(int), cudaMemcpyDeviceToHost);

    /* Free device memory */
    cudaFree(A_d);
    cudaFree(B_d);
    cudaFree(C_d);
}

} /* extern "C" */