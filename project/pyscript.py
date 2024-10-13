import subprocess
from typing import List
import pandas as pd
import seaborn as sns

factors = {
    'MATSIZE': [2**i for i in range(1,4)],
    'PATTERNS_SIZE': [2**i for i in range(1,4)],
    'NB_PATTERNS': [2**i for i in range(4)]
}

# note : make run_release must run in the background
# from project folder :
# env matsize=64 patterns_size=64 nb_patterns=2 ../wrk2/wrk http://localhost:8888/
# --threads 2 --connections 10 --duration 10s --rate 1024 --script ./wrk_scripts/simple_scenario.lua
def launch_and_parse(**params):
    f = open("output.txt", "w")
    output = subprocess.check_output([
        'env',
        'matsize='+str(params["MATSIZE"]),
        'patterns_size='+str(params["PATTERNS_SIZE"]),
        'nb_patterns='+str(params["NB_PATTERNS"]),
        '../wrk2/wrk',
        'http://localhost:8888/',
        '--threads', '4',
        '--connections', '5',
        '--rate', '1024',
        '--duration', '10s',
        '--latency',
        '--script', './wrk_scripts/simple_scenario.lua'
    ])
    f.write(str(output))
    f.close()
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
print(x)
print(series)

# g = sns.catplot(
#     data=results, kind="bar",
#     x=x[0], y="Y", hue=series[0],
#     errorbar="sd"
# )
