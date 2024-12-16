#!/bin/bash

# sudo make -B run_release_simd CFLAGS+="-DSIMD128" NB_WORKER=1
# env matsize=128 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --duration 10s --rate -1 -s wrk_scripts/simple_scenario.lua | grep "Requests/sec" | awk '{print "Basic," $2}'

N=10 # number of rounds
MATSIZE=128
NB_PATTERNS=2
PATTERNS_SIZE=64
RATE=-1
SIMDS=( "SIMD128" "SIMD256" "SIMD512" ) # "SIMD512"

# Create the csv and add header
CSV="SIMD.csv"
echo "CFLAG,Requests/sec" > $CSV

# Basic run
make -B -C server_implementation/ run_release NB_WORKER=1 &
sleep 2
#echo "===== Basic ====="
for i in $(seq 1 $N); do
#    echo -n "Basic | Run ${i} "
    RES=$(env matsize=$MATSIZE patterns_size=$PATTERNS_SIZE nb_patterns=$NB_PATTERNS ../wrk2/wrk http://localhost:8888/ --duration 10s --rate $RATE \
        -s wrk_scripts/simple_scenario.lua | grep "Requests/sec" | awk '{print "Basic," $2}')
#    echo "$RES" | awk -F',' '{print "=> " $2 " Requests/sec"}'
    echo "$RES" >> $CSV
done

# Best run
make -B -C server_implementation/ run_release CFLAGS+="-DBEST" NB_WORKER=1 &
sleep 2
#echo "===== Best ====="
for i in $(seq 1 $N); do
#    echo -n "Best | Run ${i} "
    RES=$(env matsize=$MATSIZE patterns_size=$PATTERNS_SIZE nb_patterns=$NB_PATTERNS ../wrk2/wrk http://localhost:8888/ --duration 10s --rate $RATE \
        -s wrk_scripts/simple_scenario.lua | grep "Requests/sec" | awk '{print "Best," $2}')
#    echo "$RES" | awk -F',' '{print "=> " $2 " Requests/sec"}'
    echo "$RES" >> $CSV
done

# SIMD128, SIMD256 and SIMD512 run
for SIMD in "${SIMDS[@]}"; do
    make -B -C server_implementation/ run_release_simd CFLAGS+="-D$SIMD" NB_WORKER=1 &
    sleep 2
#    echo "===== ${SIMD} ====="
    for i in $(seq 1 $N); do
#        echo -n "${SIMD} | Run ${i} "
        RES=$(env matsize=$MATSIZE patterns_size=$PATTERNS_SIZE nb_patterns=$NB_PATTERNS ../wrk2/wrk http://localhost:8888/ --duration 10s --rate $RATE \
                -s wrk_scripts/simple_scenario.lua | grep "Requests/sec" | awk -v SIMD="$SIMD" '{print SIMD "," $2}')
#        echo "$RES" | awk -F',' '{print "=> " $2 " Requests/sec"}'
        echo "$RES" >> $CSV
    done
done

# Generate graph.png
python3 plot.py
