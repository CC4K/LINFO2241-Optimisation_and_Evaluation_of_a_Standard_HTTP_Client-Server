import subprocess
import pandas as pd
import csv
import re

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
        # '--connections', str(params["connections"]),
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
# Test case 1: Small and big matrices
print("Test case 1: Small and big matrices")
print("-----------------------------------")

factors1 = {
    'MATSIZE': [64, 512],
    'NB_PATTERNS': [1],
    'PATTERNS_SIZE': [4],
    'rate': [-1],
    'duration': [30]
    # 'connections': [2]
}

df = design_experiment(factors1)
repeat_count = 3

with open('test1.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['MATSIZE', 'NB_PATTERNS', 'PATTERNS_SIZE', 'Requests/sec'])
    for i in range(len(df)):
        df_params = df.iloc[i]
        params = df_params.to_dict()
        if (i < 0): continue
        try:
            request = []
            print("MATSIZE = " + str(params["MATSIZE"]) + " | NB_PATTERNS = " + str(params["NB_PATTERNS"]) + " | PATTERNS_SIZE = " + str(params["PATTERNS_SIZE"]))
            for j in range(repeat_count):
                # print("Test n°" + str(i+1) + " | Repeat n°" + str(j+1))
                out = launch_and_parse(**params)
                # only keep the line that starts with Requests/sec:
                out = out.decode("utf-8").split("\n")
                # print(out)
                request_per_second = -1
                for line in out:
                    if line.startswith("Requests/sec:"):
                        match = re.search(r'[-+]?\d*\.\d+|\d+', line)
                        request_per_second = float(match.group())
                # print("Request/sec of current run: " + str(request_per_second))
                request.append(request_per_second)
            rps = round(sum(request)/repeat_count, 3)
            # print("=> Mean of Request/sec: " + str(rps) + " <=")
            writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], rps])
            if (rps <= 0):
                print("test failed"+str(params))
        except Exception as e:
            writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], -1])

#================================================================================================#
# Test case 2: Small and big patterns
print("\nTest case 2: Small and big patterns")
print("-----------------------------------")

factors2 = {
    'MATSIZE': [64],
    'NB_PATTERNS': [16],
    'PATTERNS_SIZE': [32, 128],
    'rate': [-1],
    'duration': [30]
    # 'connections': [2]
}

df = design_experiment(factors2)
repeat_count = 3

with open('test2.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['MATSIZE', 'NB_PATTERNS', 'PATTERNS_SIZE', 'Requests/sec'])
    for i in range(len(df)):
        df_params = df.iloc[i]
        params = df_params.to_dict()
        if (i < 0): continue
        try:
            request = []
            print("MATSIZE = " + str(params["MATSIZE"]) + " | NB_PATTERNS = " + str(params["NB_PATTERNS"]) + " | PATTERNS_SIZE = " + str(params["PATTERNS_SIZE"]))
            for j in range(repeat_count):
                print("Test n°" + str(i+1) + " | Repeat n°" + str(j+1))
                out = launch_and_parse(**params)
                # only keep the line that starts with Requests/sec:
                out = out.decode("utf-8").split("\n")
                # print(out)
                request_per_second = -1
                for line in out:
                    if line.startswith("Requests/sec:"):
                        match = re.search(r'[-+]?\d*\.\d+|\d+', line)
                        request_per_second = float(match.group())
                # print("Request/sec of current run: " + str(request_per_second))
                request.append(request_per_second)
            rps = round(sum(request)/repeat_count, 3)
            # print("=> Mean of Request/sec: " + str(rps) + " <=")
            writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], rps])
            if (rps <= 0):
                print("test failed"+str(params))
        except Exception as e:
            writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], -1])

#================================================================================================#
# Test case 3: Small and large amount of patterns
print("\nTest case 3: Small and large amount of patterns")
print("-----------------------------------------------")

factors3 = {
    'MATSIZE': [64],
    'NB_PATTERNS': [8, 128],
    'PATTERNS_SIZE': [32],
    'rate': [-1],
    'duration': [30]
    # 'connections': [2]
}

df = design_experiment(factors3)
repeat_count = 3

with open('test3.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['MATSIZE', 'NB_PATTERNS', 'PATTERNS_SIZE', 'Requests/sec'])
    for i in range(len(df)):
        df_params = df.iloc[i]
        params = df_params.to_dict()
        if (i < 0): continue
        try:
            request = []
            print("MATSIZE = " + str(params["MATSIZE"]) + " | NB_PATTERNS = " + str(params["NB_PATTERNS"]) + " | PATTERNS_SIZE = " + str(params["PATTERNS_SIZE"]))
            for j in range(repeat_count):
                # print("Test n°" + str(i+1) + " | Repeat n°" + str(j+1))
                out = launch_and_parse(**params)
                # only keep the line that starts with Requests/sec:
                out = out.decode("utf-8").split("\n")
                # print(out)
                request_per_second = -1
                for line in out:
                    if line.startswith("Requests/sec:"):
                        match = re.search(r'[-+]?\d*\.\d+|\d+', line)
                        request_per_second = float(match.group())
                # print("Request/sec of current run: " + str(request_per_second))
                request.append(request_per_second)
            rps = round(sum(request)/repeat_count, 3)
            # print("=> Mean of Request/sec: " + str(rps) + " <=")
            writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], rps])
            if (rps <= 0):
                print("test failed"+str(params))
        except Exception as e:
            writer.writerow([params["MATSIZE"], params["NB_PATTERNS"], params["PATTERNS_SIZE"], -1])
