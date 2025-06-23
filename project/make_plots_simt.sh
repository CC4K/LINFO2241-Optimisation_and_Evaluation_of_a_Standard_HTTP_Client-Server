#!/bin/bash

mkdir -p measurements/


COMBINED_OUTPUT="measurements/test_case_CUDA.csv"
> "$COMBINED_OUTPUT"


run_tests() {
    local i=$1
    sleep 3
    python3 ./test_cuda.py $i
    make -C server_implementation/ kill_nginx > /dev/null
    wait
    if [ "$first_file" = true ]; then
        cat "test_cuda.csv" > "$COMBINED_OUTPUT"
        first_file=false
    else
        tail -n +2 "test_cuda.csv" >> "$COMBINED_OUTPUT"
    fi
    # python3 parse_perf.py 1 $i
    # mv test_cuda.csv test_cuda_$i.csv
}


# #==================== CUDA NORMAL ====================#
first_file=true

for i in 4 8 16; 
do
    (make -B -C server_implementation/ run_release_simt NVCCFLAGS+="-DCUDA_BLOCK_SIZE=$i" \
    > /dev/null) &
    run_tests $i
done


# #==================== UNOPTIMIZED ====================#
(make -B -C server_implementation/ run_release\
> /dev/null) &
run_tests "normal"

# #==================== OPTIMIZED ====================#
(make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" \
> /dev/null) &
run_tests "best"

rm ./test_cuda.csv

python3 plot_cuda.py