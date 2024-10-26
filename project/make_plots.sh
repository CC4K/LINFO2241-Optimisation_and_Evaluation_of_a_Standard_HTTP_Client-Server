#!/bin/bash

# Step 1 : run python test script to test and create .csv with parameters and results
# Step 2 : save .csv in project/ folder
# Step 3 : create project/measurements folder if it doesn't exist
mkdir -p measurements/;
# Step 4 : run python plot script to plot graphs and save them in project/measurements
python3 ./plot.py
