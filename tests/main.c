#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

int main() {
    struct parsed_request parsed;
    char request[] = "2,1,2,abcdefghijklmnoabcdefghijklmnoabcdefghab";
    size_t request_len = sizeof(request) - 1;

    parse_request(&parsed, request, request_len);

    printf("Matrices size: %u\n", parsed.matrices_size);
    printf("Number of patterns: %u\n", parsed.nb_patterns);
    printf("Patterns size: %u\n", parsed.patterns_size);

    // print parsed mat1 and mat2
    printf("Matrix 1 data: ");
    for (uint32_t i = 0; i < parsed.matrices_size * parsed.matrices_size; i++) {
        printf("%c", (char)parsed.mat1[i]);
    }
    printf("\n");

    printf("Matrix 2 data: ");
    for (uint32_t i = 0; i < parsed.matrices_size * parsed.matrices_size; i++) {
        printf("%c", (char)parsed.mat2[i]);
    }
    printf("\n");

    printf("Patterns data: ");
    for (uint32_t i = 0; i < parsed.patterns_size; i++) {
        printf("%c", (char)parsed.patterns[i]);
    }
    printf("\n");

    return 0;
}

