#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "../project/utils/utils.h"

//#define DUNROLL
//#define DCACHE_AWARE
// #define BEST

void test_multiply_matrix() {
    // initialization
    uint32_t K = 8;
    uint32_t *matrix1 = malloc(K * K * sizeof(uint32_t));
    for (uint32_t i = 0; i < K * K; i++) {
        matrix1[i] = i+1;
    }
    uint32_t *matrix2 = malloc(K * K * sizeof(uint32_t));
    for (uint32_t i = 0; i < K * K; i++) {
        matrix2[i] = i+(K*K)+1;
    }
    uint32_t *intermediary_matrix = malloc(K * K * sizeof(uint32_t));

    // run function
    multiply_matrix(matrix1, matrix2, intermediary_matrix, K);

    // print result and compare
    for (uint32_t i = 1; i < (K * K)+1; i++) {
        printf("%d\t", intermediary_matrix[i-1]);
        if (i % 8 == 0) printf("\n");
    }
    printf("\n");
    printf("3684\t3720\t3756\t3792\t3828\t3864\t3900\t3936\t\n"
           "9636\t9736\t9836\t9936\t10036\t10136\t10236\t10336\t\n"
           "15588\t15752\t15916\t16080\t16244\t16408\t16572\t16736\t\n"
           "21540\t21768\t21996\t22224\t22452\t22680\t22908\t23136\t\n"
           "27492\t27784\t28076\t28368\t28660\t28952\t29244\t29536\t\n"
           "33444\t33800\t34156\t34512\t34868\t35224\t35580\t35936\t\n"
           "39396\t39816\t40236\t40656\t41076\t41496\t41916\t42336\t\n"
           "45348\t45832\t46316\t46800\t47284\t47768\t48252\t48736\n");
    uint32_t compare[64] = {3684,3720,3756,3792,3828,3864,3900,3936,9636,9736,9836,9936,10036,10136,10236,10336,15588,15752,15916,16080,16244,16408,16572,16736,21540,21768,21996,22224,22452,22680,22908,23136,27492,27784,28076,28368,28660,28952,29244,29536,33444,33800,34156,34512,34868,35224,35580,35936,39396,39816,40236,40656,41076,41496,41916,42336,45348,45832,46316,46800,47284,47768,48252,48736};
    int err = 0;
    for (uint32_t i = 0; i < 64; i++) {
        if (intermediary_matrix[i] != compare[i]) err = 1;
    }
    if (err) printf("\nIncorrect output\n");
    else printf("\nCorrect output\n");

    // end test
    free(matrix1);
    free(matrix2);
    free(intermediary_matrix);
}

void test_test_patterns() {
    // initialize
    uint32_t intermediary_matrix[64] = {3684,3720,3756,3792,3828,3864,3900,3936,9636,9736,9836,9936,10036,10136,10236,10336,15588,15752,15916,16080,16244,16408,16572,16736,21540,21768,21996,22224,22452,22680,22908,23136,27492,27784,28076,28368,28660,28952,29244,29536,33444,33800,34156,34512,34868,35224,35580,35936,39396,39816,40236,40656,41076,41496,41916,42336,45348,45832,46316,46800,47284,47768,48252,48736};
    uint32_t matrices_size = 8;
    uint32_t *patterns = malloc(16*sizeof(uint32_t));
    for (uint32_t i = 0; i < 16; i++) patterns[i] = i+1;
    uint32_t patterns_size = 16;
    uint32_t nb_patterns = 2;
    uint32_t *res_uint = malloc(nb_patterns*sizeof(uint32_t));

    // run
    test_patterns(intermediary_matrix, matrices_size, patterns, patterns_size, nb_patterns, res_uint);

    // print res_uint
    uint32_t expected[2] = {93512024, 3439283};
    int err = 0;
    for (uint32_t i = 0; i < nb_patterns; i++) {
        printf("%d\t", res_uint[i]);
        if (res_uint[i] != expected[i]) err = 1;
    }
    printf("\n\n");
    for (uint32_t i = 0; i < nb_patterns; i++) printf("%d\t", expected[i]);
    printf("\n");
    if (err) printf("\nIncorrect output\n");
    else printf("\nCorrect output\n");

    // free
    free(patterns);
    free(res_uint);
}

void parse_request_test(){
    struct parsed_request parsed;
    char request[] = "2,2,1,ThisIsAnExample!SomeNetworkLayerExamJump";
    size_t request_len = sizeof(request) - 1;

    parse_request(&parsed, request, request_len);
    printf("\nCorrect output\n");
}

int main() {
    for (size_t i = 0; i < 1000000; i++)
    {
        parse_request_test();
        // test_multiply_matrix();
    }
    

    // test_test_patterns();

    return 0;
}

// useful run commands :
// gcc main.c -o main
// gcc -g -ggdb -fPIC -Wextra -Werror -Wall -pedantic  main.c -o main
// gdb ./main
// sudo perf stat ./main
// sudo perf stat -e cache-misses,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores ./main
