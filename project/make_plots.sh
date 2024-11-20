#!/bin/bash
mkdir -p measurements/

# no opti for case 1, 2, 3
make -B -C server_implementation/ run_release &
python3 ./server_testing.py
#python3 ./plot.py #<= A DECOMMENTER QUAND plot SCRIPT TERMINE !!!

# cache aware for case 1, 2, 3
make -B -C server_implementation/ run_release "CFLAGS+=-DCACHE_AWARE" &
python3 ./server_testing.py
#python3 ./plot.py #<= A DECOMMENTER QUAND plot SCRIPT TERMINE !!!

# loop unrolling for case 1, 2, 3
make -B -C server_implementation/ run_release "CFLAGS+=-DUNROLL" &
python3 ./server_testing.py
#python3 ./plot.py #<= A DECOMMENTER QUAND plot SCRIPT TERMINE !!!

# best opti for case 1, 2, 3
make -B -C server_implementation/ run_release "CFLAGS+=-DBEST" &
python3 ./server_testing.py
#python3 ./plot.py #<= A DECOMMENTER QUAND plot SCRIPT TERMINE !!!
