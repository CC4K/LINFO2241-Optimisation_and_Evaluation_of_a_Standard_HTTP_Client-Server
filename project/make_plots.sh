#!/bin/bash
# Step 1 : start server
make -C server_implementation/ run_release &
# Step 2 : run python test script to test and create .csv with parameters and results and save it in project/ folder
python3 ./server_testing.py
# Step 3 : create project/measurements folder if it doesn't exist
mkdir -p measurements/
# Step 4 : run python plot script to plot graphs and save them in project/measurements
python3 ./plot.py
