#include <math.h>
#include <ngx_link_func_module.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utils.h"
#if defined SIMD
#include "simd.h"
#elif defined SIMT
#include "simt.h"
#endif

int is_service_on = 0;

/**
 * @brief Process the request's body, and return a response. This is the
 * function you should implement.
 *
 * @param ctx The context of the request, only used for logging and memory
 * allocation.
 * @param body The request's body, as a string.
 * @param body_len The length of the request's body.
 * @param resp_len The length of the response.
 *
 * @note You will do the required operations based on the request's body, and
 * return a response. BE CAREFUL, you MUST store the length of your response in
 * `resp_len` before returning.
 *
 * @note Also, this environment keeps you from doing classical `malloc` to
 * allocate memory. Instead, use the function `ngx_link_func_palloc(ctx,
 * number_of_bytes)`. You can also use `ngx_link_func_pcalloc(ctx, number_of_bytes)` 
 * instead of `calloc`. The advantage of this method is that your memory
 * allocation is linked to the request and everything is freed when the resquest
 * finished. No need to worry about freeing memory :)
 */

static char *body_processing(ngx_link_func_ctx_t *ctx, char *body, size_t body_len,
                             size_t *resp_len) {
    /**
     * TODO: Replace the example code below with your own code.
     */

    // Simply example that always responds with "Hello, World!"
    // You can define your functions in utils.h and utils.c, and use them here.
    (void)body;
    (void)body_len;
    int bar = foo();
    printf("bar: %d\n", bar);
    char hello_world[] = "Hello, World!\n";
    char *res = ngx_link_func_palloc(ctx, sizeof(hello_world) + 1);
    strcpy(res, hello_world);
    *resp_len = strlen(res);
    return (char *)res;
}

void main_function(ngx_link_func_ctx_t *ctx) {
    // Retrieve request's body
    char *body = (char *)ctx->req_body;
    size_t body_len = ctx->req_body_len;

    // Process the request's body
    size_t resp_len = 0;
    char *resp = body_processing(ctx, body, body_len, &resp_len);
    // Warn user in case of error during processing
    if (resp == NULL) {
        ngx_link_func_write_resp(ctx, 500, "500 Internal Server Error", "text/plain",
                                 "Failed to parse request's body",
                                 sizeof("Failed to parse request's body") - 1);
        return;
    }
    // Warn user if he forgot to set the response's length
    if (resp_len == 0) {
        ngx_link_func_write_resp(ctx, 500, "500 Internal Server Error", "text/plain",
                                 "You forgot to set the response's length ! :angry:",
                                 sizeof("You forgot to set the response's length ! :angry:") - 1);
        return;
    }
    // Return the response
    ngx_link_func_write_resp(ctx, 200, "200 OK", "text/plain", resp, resp_len);
}

/**
 * A function that is called when the application is started.
 *
 * You shouldn't do anything here
 */
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpedantic"
void ngx_link_func_init_cycle(ngx_link_func_cycle_t *cycle) {
    ngx_link_func_cyc_log(info, cycle, "%s", "Starting application, new logs !");
    is_service_on = 1;
#ifdef SIMT
    cudaError_t err;
    err = cudaInitDevice(0,0,0);
    if (err != cudaSuccess) printf("Error while initializing CUDA in cudaInitDevice: %s\n", cudaGetErrorString(err));
    err = cudaSetDevice(0);
    if (err != cudaSuccess) printf("Error while initializing CUDA in cudaSetDevice: %s\n", cudaGetErrorString(err));
#endif
}

/**
 * A function that is called when the application is stopped.
 *
 * You shouldn't do anything here
 */
void ngx_link_func_exit_cycle(ngx_link_func_cycle_t *cyc) {
    ngx_link_func_cyc_log(info, cyc, "%s\n", "Shutting down/reloading the Application");
    is_service_on = 0;
}
#pragma GCC diagnostic pop
