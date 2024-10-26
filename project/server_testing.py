import subprocess
import pandas as pd

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

repeat_count = 3
df = design_experiment()

print("df made")
# print first row of df
import csv
import re


with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['MATSIZE', 'PATTERNS_SIZE', 'NB_PATTERNS', 'THREADS', 'CONNECTIONS', 'DURATION', 'RATE', 'Requests/sec', 'Transfer/sec'])
    for i in range(len(df)):
        df_params = df.iloc[i]
        params = df_params.to_dict()
        if(i<0):
            continue
        if(params["MATSIZE"]**2<params["PATTERNS_SIZE"]+1):
            continue
        if(params["threads"]>params["connections"]):
            continue
        try:
            request = []
            transfer = []
            for j in range(repeat_count):
                print("Test n°"+str(i)+"| Repeat n°"+str(j+1))
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
                request.append(request_per_second)
                transfer.append(transfer_per_second)
            rps = sum(request)/repeat_count
            tps = sum(transfer)/repeat_count
            # print("Request/sec : "+str(request_per_second)+" / Transfer/sec : "+str(transfer_per_second))
            writer.writerow([params["MATSIZE"], params["PATTERNS_SIZE"], params["NB_PATTERNS"],params["threads"],params["connections"],params["duration"],params["rate"] , rps, tps])
            if(rps<=0):
                print("test failed"+str(params))
        except Exception as e:
            writer.writerow([params["MATSIZE"], params["PATTERNS_SIZE"], params["NB_PATTERNS"],params["threads"],params["connections"],params["duration"],params["rate"] , -1, -1])

