#!/bin/bash
mkdir -p measurements/

# no opti for case 1, 2, 3
make -B -C server_implementation/ run_release &
python3 ./server_testing.py
mv test_case1.csv test_case1_basic.csv
mv test_case2.csv test_case2_basic.csv
mv test_case3.csv test_case3_basic.csv

# cache aware for case 1, 2, 3
make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" &
python3 ./server_testing.py
mv test_case1.csv test_case1_cache_aware.csv
mv test_case2.csv test_case2_cache_aware.csv
mv test_case3.csv test_case3_cache_aware.csv

# loop unrolling for case 1, 2, 3
make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" &
python3 ./server_testing.py
mv test_case1.csv test_case1_unrolled.csv
mv test_case2.csv test_case2_unrolled.csv
mv test_case3.csv test_case3_unrolled.csv

# best opti for case 1, 2, 3
make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" &
python3 ./server_testing.py
mv test_case1.csv test_case1_best.csv
mv test_case2.csv test_case2_best.csv
mv test_case3.csv test_case3_best.csv

# plots
#python3 ./plot.py #<= A DECOMMENTER QUAND plot SCRIPT TERMINE !!!
