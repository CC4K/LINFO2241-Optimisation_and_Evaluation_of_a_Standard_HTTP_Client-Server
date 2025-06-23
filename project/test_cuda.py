import sys
import subprocess
import pandas as pd
import csv
import re

duration = 10
repeat_count = 5

def launch_and_parse(**params):
    output = subprocess.check_output([
        'env',
        'matsize='+str(params["MATSIZE"]),
        'nb_patterns='+str(params["NB_PATTERNS"]),
        'patterns_size='+str(params["PATTERNS_SIZE"]),
        '../wrk2/wrk',
        'http://localhost:8888/',
        '--rate', str(params["rate"]),
        '--duration', str(params["duration"])+'s',
        '--connections', str(params["connections"]),
        '-t', '1',
        '--latency',
        '--script', './wrk_scripts/simple_scenario.lua'
        
    ])
    return output

def design_experiment(factors):
    X=[]
    for factor,levels in factors.items():
        newX = []
        for l in levels:
            if X:
                for run in X:
                    nr = run.copy()
                    nr.append(l)
                    newX.append(nr)
            else:
                newX.append([l])
        X = newX
    return pd.DataFrame(X, columns = factors.keys())

#================================================================================================#
# Test case cuda
def test_cuda(cuda_block_size):
    # print("Test case CUDA")
    # print("-----------------------------------")

    factors1 = {
        'MATSIZE': [128],
        'NB_PATTERNS': [2],
        'PATTERNS_SIZE': [64],
        'rate': [-1],
        'duration': [duration],
        'connections': [1]
    }

    df = design_experiment(factors1)

    with open('test_cuda.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['MATSIZE', 'NB_PATTERNS', 'PATTERNS_SIZE', 'Requests/sec','Settings'])
        for i in range(len(df)):
            df_params = df.iloc[i]
            params = df_params.to_dict()
            if (i < 0): continue
            try:
                request = []
                # print("MATSIZE = " + str(params["MATSIZE"]) + " | NB_PATTERNS = " + str(params["NB_PATTERNS"]) + " | PATTERNS_SIZE = " + str(params["PATTERNS_SIZE"]))
                for _ in range(repeat_count):
                    out = launch_and_parse(**params)
                    out = out.decode("utf-8").split("\n")
                    request_per_second = -1
                    for line in out:
                        if line.startswith("Requests/sec:"):
                            match = re.search(r'[-+]?\d*\.\d+|\d+', line)
                            request_per_second = float(match.group())
                    request.append(request_per_second)
                for item in request:
                    writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], item,cuda_block_size])
            except Exception as e:
                writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], -1,cuda_block_size])


if len(sys.argv) > 1:
    test_cuda(sys.argv[1])
else:
    print("test_cuda.py: Python argument is missing")
    sys.exit(1)


