#include <assert.h>
#include "../project/utils/utils.h"

int main() {
    
    // parsing
    struct parsed_request parsed;
    char request[] = "2,2,1,ThisIsAnExample!SomeNetworkLayerExamJump";
    size_t request_len = sizeof(request) - 1;

    parse_request(&parsed, request, request_len);

    printf("Matrices size: %u\n", parsed.matrices_size);
    printf("Number of patterns: %u\n", parsed.nb_patterns);
    printf("Patterns size: %u\n", parsed.patterns_size);
    // print parsed mat1 and mat2
    printf("Matrix 1 data: ");
    for (uint32_t i = 0; i < parsed.matrices_size * parsed.matrices_size; i++) {
        printf("%d ", parsed.mat1[i]);
    }
    printf("\n");
    printf("Matrix 2 data: ");
    for (uint32_t i = 0; i < parsed.matrices_size * parsed.matrices_size; i++) {
        printf("%d ", parsed.mat2[i]);
    }
    printf("\n");
    printf("Patterns data: ");
    for (uint32_t i = 0; i < parsed.nb_patterns; i++) {
        printf("%d ", parsed.patterns[i]);
    }
    // printf("\n\n");
     
    //  test multiply
    uint32_t *result = (uint32_t *) malloc(16*sizeof(uint32_t));
    multiply_matrix(parsed.mat1, parsed.mat2, result, parsed.matrices_size);

    uint32_t expected_result[16] = {2120728035, -965862079, 1614073327, -1706498954, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    printf("Result: ");
    for (uint32_t i = 0; i < 16; i++) {
        printf("%d ", result[i]); 
        assert(result[i] == expected_result[i]);
    }

    
    // test_patterns
    uint32_t *res = (uint32_t *) malloc(UINT32_MAX);
    uint32_t matrix[16] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
    uint32_t matrix_size = 4;
    uint32_t patterns_size = 8;
    uint32_t nb_patterns = 3;
    uint32_t patterns[24] = {10,20,3,4,50,6,70,8,9,10,11,12,130,14,150,16,170,18,19,200,21,220,23,24};

    test_patterns(matrix, matrix_size, patterns, patterns_size, nb_patterns, res);
    uint32_t expected_res[3] = {4751, 31914, 104021};

    printf("res : ");
    for (uint32_t i = 0; i < nb_patterns; i++) {
        printf("%d ", res[i]);
        assert(res[i] == expected_res[i]);
    }
    printf("\n\n");
     

    // // 2,1,2,abcdefghijklmnoabcdefghijklmnoabcdefghab
    // char *res_str = (char*) malloc(65536*sizeof(char));
    // // //Available intermediary storage use them
    // uint32_t *res_uint = (uint32_t*) malloc(1024*sizeof(uint32_t));
    // uint32_t *intermediary_matrix = (uint32_t*) malloc(1024*sizeof(uint32_t));
    // uint32_t *resp_len = (uint32_t*) malloc(sizeof(uint32_t));
    
    // char *request = "2,2,2,abcdefghijklmnoabcdefghijklmnoabcdefghababcdefgh";
    // char *response = complete_algorithm(request, strlen(request), res_str, res_uint, intermediary_matrix, resp_len);

    // printf("%s\n", res_str);
    // // printf("%s\n", response);
    // printf("length: %d\n", *resp_len);

    return 0;
}

