#!/bin/bash

mkdir -p measurements/

# #==================== Test case 1, 2, 3 ====================#


# #======== BASIC #========

run_tests() {
    case_name=$1
    cflags=$2

    echo "Case 1, 2, 3, ${case_name} optimization"

    for i in 1 2 3; do
        (perf stat -e task-clock,cycles,instructions,branches,branch-misses,L1-dcache-loads,L1-dcache-load-misses,stalled-cycles-frontend -D 2000 \
        make -B -C server_implementation/ run_release ${cflags} \
        > "output.txt" 2>&1) &
        sleep 1
        python3 ./test_1_2_3.py $i
        make -C server_implementation/ kill_nginx
        wait
        python3 parse_perf.py 1 $i
        mv output.csv test_case$i.csv
    done

    combine_and_move_csv "${case_name}"
}

combine_and_move_csv() {
    case_name=$1

    # Extract the header from the first file
    head -n 1 test_case1.csv > combined_tests.csv

    # Append the content of all files excluding the header
    for i in 1 2 3; do
        tail -n +2 test_case$i.csv >> combined_tests.csv
        rm test_case$i.csv
    done

    mv combined_tests.csv measurements/test_case1_2_3_${case_name}.csv

    for i in 1 2 3; do
        mv test$i.csv measurements/test_case${i}_${case_name}.csv
    done
}

# Run tests for different cases
run_tests "basic" ""
run_tests "cache_aware" "CFLAGS+=-DCACHE_AWARE"
run_tests "unrolled" "CFLAGS+=-DUNROLL"
run_tests "best" "CFLAGS+=-DBEST"





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


chmod -R a+rw .
echo "End of script"