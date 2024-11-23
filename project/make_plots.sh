#!/bin/bash

mkdir -p measurements/

#==================== Test case 1, 2, 3 ====================#
echo "Case 1, 2, 3, no optimization"
make -B -C server_implementation/ run_release &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_basic.csv
mv test2.csv measurements/test_case2_basic.csv
mv test3.csv measurements/test_case3_basic.csv

echo "Case 1, 2, 3, cache awareness optimization"
make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_cache_aware.csv
mv test2.csv measurements/test_case2_cache_aware.csv
mv test3.csv measurements/test_case3_cache_aware.csv

echo "Case 1, 2, 3, loop unrolling optimization"
make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_unrolled.csv
mv test2.csv measurements/test_case2_unrolled.csv
mv test3.csv measurements/test_case3_unrolled.csv

echo "Case 1, 2, 3, best optimization"
make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" &
python3 ./test_1_2_3.py
mv test1.csv measurements/test_case1_best.csv
mv test2.csv measurements/test_case2_best.csv
mv test3.csv measurements/test_case3_best.csv



#======================= Test case 4 =======================#
echo "Test case 4: Resource utilization"
echo "---------------------------------"


echo "Case 4, no optimization"
make -B -C server_implementation/ run_release NB_WORKER=1 &
echo "NB_WORKER = 1"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic1.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release NB_WORKER=2 &
echo "NB_WORKER = 2"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic2.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release NB_WORKER=4 &
echo "NB_WORKER = 4"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic3.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release NB_WORKER=8 &
echo "NB_WORKER = 8"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_basic4.csv
make -C server_implementation/ kill_nginx
wait


echo "Case 4, cache awareness optimization"
make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=1 &
echo "NB_WORKER = 1"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware1.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=2 &
echo "NB_WORKER = 2"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware2.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=4 &
echo "NB_WORKER = 4"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware3.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" NB_WORKER=8 &
echo "NB_WORKER = 8"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_cache_aware4.csv
make -C server_implementation/ kill_nginx
wait


echo "Case 4, loop unrolling"
make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=1 &
echo "NB_WORKER = 1"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled1.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=2 &
echo "NB_WORKER = 2"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled2.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=4 &
echo "NB_WORKER = 4"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled3.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" NB_WORKER=8 &
echo "NB_WORKER = 8"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_unrolled4.csv
make -C server_implementation/ kill_nginx
wait


echo "Case 4, best optimization"
make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=1 &
echo "NB_WORKER = 1"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_best1.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=2 &
echo "NB_WORKER = 2"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_best2.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=4 &
echo "NB_WORKER = 4"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_best3.csv
make -C server_implementation/ kill_nginx
wait

make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" NB_WORKER=8 &
echo "NB_WORKER = 8"
echo "-------------"
python3 ./test4.py
mv test4.csv measurements/test_case4_best4.csv
make -C server_implementation/ kill_nginx
wait


echo "Evaluating with perf"...
sudo bash task4.sh


#========================== Plots ==========================#
echo "Generating plots..."
python3 ./plot.py
echo "Plots generated"
echo "End of script"
