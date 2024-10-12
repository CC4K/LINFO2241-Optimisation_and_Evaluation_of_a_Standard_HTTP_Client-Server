#!/bin/bash
# command to run test
# env matsize=64 patterns_size=64 nb_patterns=2 ./wrk2/wrk http://localhost:8888/ --threads 2 --connections 10 --rate 1024 --duration 10s --script project/wrk_scripts/simple_scenario.lua
# possible parameters :
# matsize = size of matrices
# patterns_size = size of patterns
# nb_patterns = number of patterns
# possible wrk parameters :
# --threads = total number of threads to use => CPU
# --connections = total number of http connections to keep open => network
# --rate = work rate / throughput in requests/sec => network
# --duration = duration of the test => euuuuuh
# wrk options : --latency to print latency stats (gnuplots ???) + --u_latency to print uncorrected latency stats + --timeout to set request timeout

# TODO: Make plots
