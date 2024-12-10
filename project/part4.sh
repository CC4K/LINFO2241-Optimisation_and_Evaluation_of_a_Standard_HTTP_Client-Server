#!/bin/bash

N=10 # number of rounds
MATSIZE=128
NB_PATTERNS=2
PATTERNS_SIZE=64
NB_WORKER=1
RATE=-1
CFLAGS=( "-DSIMD128" "-DSIMD256" "-DSIMD512" "-DSIMDBEST" )

# Ensure the measurements directory exists
mkdir -p measurements

for CFLAG in "${CFLAGS[@]}"; do
    # Define the combined output file for this CFLAG
    CFLAG_NAME=$(echo "$CFLAG" | sed 's/^-D//;s/_//g;') # Normalize CFLAG name for file naming
    COMBINED_OUTPUT="measurements/output_${CFLAG_NAME,,}.csv"

    [ -f $COMBINED_OUTPUT ] && rm $COMBINED_OUTPUT # Remove existing combined output file

    echo "Processing CFLAG: $CFLAG"

    for i in $(seq 1 $N); do
        echo "Running iteration $i for NB_WORKER=$NB_WORKER and CFLAG=$CFLAG"

        # Run the main experiment
        (sleep 3 && cd ../ && env matsize=$MATSIZE patterns_size=$PATTERNS_SIZE nb_patterns=$NB_PATTERNS ./wrk2/wrk \
        http://localhost:8888/ --duration 10s --rate $RATE \
        -s project/wrk_scripts/simple_scenario.lua > "output_${CFLAG}.csv" && echo "done") &

        # Generate the CSV output and rename it
        # TODO: parse "output_SIMD256_1.csv" file to keep Requests/sec only
        # python3 parse_perf.py $CFLAG
        # mv output.csv "output_${CFLAG}_${i}.csv"

#        # Add parsed output of this run to final output
#        if [ $i -eq 1 ] && [ "${NB_WORKER}" == "${NB_WORKER[0]}" ]; then
#            # Include the header for the very first file
#            cat "output_${CFLAG}_${i}.csv" >> $COMBINED_OUTPUT
#        else
#            # Skip the header for subsequent files
#            tail -n +2 "output_${CFLAG}_${i}.csv" >> $COMBINED_OUTPUT
#        fi

        # Cleanup
        rm "output.txt"
        rm "output_${CFLAG}_${i}.csv"
    done
done

echo "All iterations complete."

make -B run_release_simd CFLAGS+="-DSIMDBEST"