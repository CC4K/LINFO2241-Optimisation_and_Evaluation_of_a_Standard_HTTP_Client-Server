#!/bin/bash
mkdir -p measurements/

echo "Basic for case 1, 2, 3"
make -B -C server_implementation/ run_release &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_basic.csv
mv test2.csv measurements/test_case2_basic.csv
mv test3.csv measurements/test_case3_basic.csv
echo "Basic finished"
echo "____________________________________________________________________"

echo "Cache aware for case 1, 2, 3"
make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_cache_aware.csv
mv test2.csv measurements/test_case2_cache_aware.csv
mv test3.csv measurements/test_case3_cache_aware.csv
echo "Cache-aware finished"
echo "____________________________________________________________________"

echo "Unroll for case 1, 2, 3"
make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_unrolled.csv
mv test2.csv measurements/test_case2_unrolled.csv
mv test3.csv measurements/test_case3_unrolled.csv
echo "Unroll finished"
echo "____________________________________________________________________"

echo "Best for case 1, 2, 3"
make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_best.csv
mv test2.csv measurements/test_case2_best.csv
mv test3.csv measurements/test_case3_best.csv
echo "Best finished"
echo "____________________________________________________________________"

echo "Basic for case 4"
make -B -C server_implementation/ run_release NB_WORKER=1 &
echo "NB_WORKER = 1"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic1.csv

make -B -C server_implementation/ run_release NB_WORKER=2 &
echo "NB_WORKER = 2"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic2.csv

make -B -C server_implementation/ run_release NB_WORKER=4 &
echo "NB_WORKER = 4"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic3.csv

make -B -C server_implementation/ run_release NB_WORKER=8 &
echo "NB_WORKER = 8"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic4.csv
echo "Test case 4 basic finished"
echo "____________________________________________________________________"

echo "Cache aware for case 4"
make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=1 &
echo "NB_WORKER = 1"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware1.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=2 &
echo "NB_WORKER = 2"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware2.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=4 &
echo "NB_WORKER = 4"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware3.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=8 &
echo "NB_WORKER = 8"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware4.csv
echo "Test case 4 cache aware finished"
echo "____________________________________________________________________"

echo "Unroll for case 4"
make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=1 &
echo "NB_WORKER = 1"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled1.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=2 &
echo "NB_WORKER = 2"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled2.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=4 &
echo "NB_WORKER = 4"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled3.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=8 &
echo "NB_WORKER = 8"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled4.csv
echo "Test case 4 unrolled finished"
echo "____________________________________________________________________"

echo "Best for case 4"
make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=1 &
echo "NB_WORKER = 1"
python3 ./test4.py
mv test4.csv measurements/test_case4_best1.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=2 &
echo "NB_WORKER = 2"
python3 ./test4.py
mv test4.csv measurements/test_case4_best2.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=4 &
echo "NB_WORKER = 4"
python3 ./test4.py
mv test4.csv measurements/test_case4_best3.csv

make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=8 &
echo "NB_WORKER = 8"
python3 ./test4.py
mv test4.csv measurements/test_case4_best4.csv
echo "Test case 4 best finished"
echo "____________________________________________________________________"

echo "Generating plots..."
python3 ./plot.py
echo "Plots generated"
echo "____________________________________________________________________"
