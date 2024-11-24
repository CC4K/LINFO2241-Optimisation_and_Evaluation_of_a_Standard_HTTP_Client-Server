#!/bin/bash

N=3 # Number of repetitions
NB_WORKERS=(1 2 4 8)
CFLAGS=( "-DBASIC" "-DCACHE_AWARE" "-DUNROLL" "-DBEST" )

# Ensure the measurements directory exists
mkdir -p measurements

for CFLAG in "${CFLAGS[@]}"; do
    # Define the combined output file for this CFLAG
    CFLAG_NAME=$(echo "$CFLAG" | sed 's/^-D//;s/_//g;') # Normalize CFLAG name for file naming
    COMBINED_OUTPUT="measurements/test_case4_${CFLAG_NAME,,}.csv"

    [ -f $COMBINED_OUTPUT ] && rm $COMBINED_OUTPUT # Remove existing combined output file
    
    echo "Processing CFLAG: $CFLAG"
    
    for NB_WORKER in "${NB_WORKERS[@]}"; do
        echo "Running with NB_WORKER=$NB_WORKER and CFLAG=$CFLAG"
        
        for i in $(seq 1 $N); do
            echo "Running iteration $i for NB_WORKER=$NB_WORKER and CFLAG=$CFLAG"
            
            # Run the main experiment
            (sleep 3 && cd ../ && env matsize=512 patterns_size=8 nb_patterns=1 ./wrk2/wrk \
            http://localhost:8888/ --duration 7s -R-1 \
            -s project/wrk_scripts/simple_scenario.lua > /dev/null 2>&1 && echo "done") &
            
            echo "running perf"
            perf stat -e task-clock,cycles,instructions,branches,branch-misses,L1-dcache-loads,L1-dcache-load-misses,stalled-cycles-frontend --timeout 2000 -D 5000 make -B -C server_implementation/ run_release "CFLAGS+=$CFLAG" NB_WORKER=$NB_WORKER > "output.txt" 2>&1
            wait
            
            # Generate the CSV output and rename it
            python3 parse_perf.py $NB_WORKER 4
            mv output.csv "output_${NB_WORKER}_${i}.csv"
            
            if [ $i -eq 1 ] && [ "${NB_WORKER}" == "${NB_WORKERS[0]}" ]; then
                # Include the header for the very first file
                cat "output_${NB_WORKER}_${i}.csv" >> $COMBINED_OUTPUT
            else
                # Skip the header for subsequent files
                tail -n +2 "output_${NB_WORKER}_${i}.csv" >> $COMBINED_OUTPUT
            fi

            # Cleanup
            rm "output.txt"
            rm "output_${NB_WORKER}_${i}.csv"
        done
    done
done

echo "All iterations complete."
