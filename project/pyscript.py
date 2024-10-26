import subprocess
from typing import List
import pandas as pd
import seaborn as sns


# note : make run_release must run in the background
# from project folder :
# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --threads 2 --connections 10 --duration 10s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 234 / Transfer/sec : 36 KB

# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --threads 1 --connections 100 --duration 10s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 206 / Transfer/sec : 32 KB (connections change un toooooout petit peu)

# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --threads 1 --connections 10 --duration 10s --rate 2048 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 246 / Transfer/sec : 38 KB (augmenter rate fait augmenter)

# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --threads 1 --connections 10 --duration 10s --rate 512 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 218 / Transfer/sec : 34 KB (diminuer rate fait diminuer)

# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --threads 4 --connections 10 --duration 10s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 272 / Transfer/sec : 42 KB (threads ne change pas)

# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --threads 1 --connections 10 --duration 60s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 349 / Transfer/sec : 54 KB (duration change bcp)

# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --duration 10s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 232 / Transfer/sec : 36 KB (ref pour matrix parameters)

# env matsize=1000 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --duration 10s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 232 / Transfer/sec : 36 KB (large matsize is MUCH SLOWER (code crashed with 10000))

# env matsize=64 patterns_size=1000 nb_patterns=2 ../wrk2/wrk http://localhost:8888/ --duration 10s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 29 / Transfer/sec : 4 KB (large patterns_size is MUCH FASTER)

# env matsize=64 patterns_size=64 nb_patterns=32 ../wrk2/wrk http://localhost:8888/ --duration 10s --rate 1024 --latency --script ./wrk_scripts/simple_scenario.lua
# Request/sec : 21 / Transfer/sec : 7 KB (too much patterns crash so idk)

# paramètres importants : matsize, patterns_size, nb_patterns, rate, connections, (threads et duration bof bof on pourrait ignorer)


factors = {
'MATSIZE': [32,128,256, 512],
'PATTERNS_SIZE': [16, 64, 128],
'threads': [1, 4, 8],
'rate': [64,256, 512],

'NB_PATTERNS': [4],
'connections': [10],
'duration': [10],
# 'NB_PATTERNS': [1, 2, 4],
# 'duration': [10,20],
}



def launch_and_parse(**params):
    output = subprocess.check_output([
        'env',
        'matsize='+str(params["MATSIZE"]),
        'patterns_size='+str(params["PATTERNS_SIZE"]),
        'nb_patterns='+str(params["NB_PATTERNS"]),
        '../wrk2/wrk',
        'http://localhost:8888/',
        '--threads', str(params["threads"]),
        '--connections', str(params["connections"]),
        '--rate', str(params["rate"]),
        '--duration', str(params["duration"])+'s',
        '--latency',
        '--script', './wrk_scripts/simple_scenario.lua'
    ])
    return output
    
    
    # f.write(str(output))
    # f.close()
    # should get the number of interest

def design_experiment():
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

######################################################"

n_repetitions = 3

def launch_experiment(design) -> List[List]:
    data = []
    results = []
    for run in design.to_dict(orient="records"):
            print(f"Running {run}...")
            for repet in range(n_repetitions):
                r = launch_and_parse(**run)
                print(r)
                run_result = list(run.values()).copy()
                run_result.append(r)
                results.append(run_result)
    return results

# runs = design_experiment()
# print(runs)
# results = launch_experiment(runs)
# results = pd.DataFrame(results, columns=list(factors.keys())+ ['Y'])
# print(results)

################

#The first factor is used for the X axis
x = list(factors.items())[0]
#The second factor is used as series
series = list(factors.items())[1]
# print(x)
# print(series)

# g = sns.catplot(
#     data=results, kind="bar",
#     x=x[0], y="Y", hue=series[0],
#     errorbar="sd"
# )

# for factor in factors:
    # print(factors[factor])
    # print(subprocess.run(["pwd"]))
    
repeat_count = 3
df = design_experiment()

print("df made")
# print first row of df
import csv
import re


with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['MATSIZE', 'PATTERNS_SIZE', 'NB_PATTERNS', 'THREADS', 'CONNECTIONS', 'DURATION', 'RATE', 'Requests/sec', 'Transfer/sec'])
    for j in range(repeat_count):    
        for i in range(len(df)):
            print("i: "+str(i)+" j: "+str(j))
            df_params = df.iloc[i]
            params = df_params.to_dict()
            if(i<0):
                continue
            if(params["MATSIZE"]**2<params["PATTERNS_SIZE"]+1):
                continue
            if(params["threads"]>params["connections"]):
                continue
            try:
                out = launch_and_parse(**params)
                # only keep the line that starts with Requests/sec:
                out = out.decode("utf-8").split("\n")
                # print(out)
                request_per_second = -1
                transfer_per_second = -1
                for line in out:
                    if line.startswith("Requests/sec:"):
                        match = re.search(r'[-+]?\d*\.\d+|\d+', line)
                        request_per_second = float(match.group())
                    if line.startswith("Transfer/sec:"):
                        match = line.split("Transfer/sec:")[1].replace(' ','')
                        transfer_per_second = match
                # print("Request/sec : "+str(request_per_second)+" / Transfer/sec : "+str(transfer_per_second))
                writer.writerow([params["MATSIZE"], params["PATTERNS_SIZE"], params["NB_PATTERNS"],params["threads"],params["connections"],params["duration"],params["rate"] , request_per_second, transfer_per_second])
                if(request_per_second<=0):
                    print("test failed"+str(params))
            except Exception as e:
                writer.writerow([params["MATSIZE"], params["PATTERNS_SIZE"], params["NB_PATTERNS"],params["threads"],params["connections"],params["duration"],params["rate"] , -1, -1])

