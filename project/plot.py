import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({"figure.max_open_warning": 0})
sns.set_theme(style="darkgrid")


#============= Test case 1, 2, 3 =============#

# Load all the CSV file with pandas and add optimisation flags and test sizes
df_1_0 = pd.read_csv("measurements/test_case1_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_0 = df_1_0.assign(Flag = ["No optimisation"]*2)
df_1_1 = pd.read_csv("measurements/test_case1_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_1 = df_1_1.assign(Flag = ["Cache awareness"]*2)
df_1_2 = pd.read_csv("measurements/test_case1_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_2 = df_1_2.assign(Flag = ["Loop unrolling"]*2)
df_1_3 = pd.read_csv("measurements/test_case1_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_3 = df_1_3.assign(Flag = ["Best optimisation"]*2)

df_2_0 = pd.read_csv("measurements/test_case2_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_0 = df_2_0.assign(Flag = ["No optimisation"]*2)
df_2_1 = pd.read_csv("measurements/test_case2_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_1 = df_2_1.assign(Flag = ["Cache awareness"]*2)
df_2_2 = pd.read_csv("measurements/test_case2_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_2 = df_2_2.assign(Flag = ["Loop unrolling"]*2)
df_2_3 = pd.read_csv("measurements/test_case2_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_3 = df_2_3.assign(Flag = ["Best optimisation"]*2)

df_3_0 = pd.read_csv("measurements/test_case3_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_0 = df_3_0.assign(Flag = ["No optimisation"]*2)
df_3_1 = pd.read_csv("measurements/test_case3_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_1 = df_3_1.assign(Flag = ["Cache awareness"]*2)
df_3_2 = pd.read_csv("measurements/test_case3_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_2 = df_3_2.assign(Flag = ["Loop unrolling"]*2)
df_3_3 = pd.read_csv("measurements/test_case3_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_3 = df_3_3.assign(Flag = ["Best optimisation"]*2)

# combine by test case
df_case1 = pd.concat([df_1_0, df_1_1, df_1_2, df_1_3], axis=0)
df_case2 = pd.concat([df_2_0, df_2_1, df_2_2, df_2_3], axis=0)
df_case3 = pd.concat([df_3_0, df_3_1, df_3_2, df_3_3], axis=0)
# print(df_case1.to_string())
# print(df_case2.to_string())
# print(df_case3.to_string())

colors = ['red', 'orange', 'yellow', 'green']

#================ Test case 1 ================#
plt.figure() # different matrix sizes
res = sns.barplot(data=df_case1, x="MATSIZE", y="Requests/sec", hue="Flag", palette=colors, edgecolor='black')
for i in res.containers: res.bar_label(i, fontsize=6.5)
plt.legend(title="Optimisation method")
plt.xlabel("Matrix Sizes")
plt.ylabel("Requests/sec")
plt.title("Requests/sec by matrix sizes for every optimisation method (log scale)")
plt.yscale('log')

plt.savefig("measurements/barplot_result1.pdf", format="pdf")
# plt.savefig("measurements/barplot_result1.png")
print("barplot_result1 generated")

#================ Test case 2 ================#
plt.figure() # different patterns sizes
res = sns.barplot(data=df_case2, x="PATTERNS_SIZE", y="Requests/sec", hue="Flag", palette=colors, edgecolor='black')
for i in res.containers: res.bar_label(i, fontsize=6.5)
plt.legend(title="Optimisation method")
plt.xlabel("Patterns Sizes")
plt.ylabel("Requests/sec")
plt.title("Requests/sec by patterns sizes for every optimisation method")
plt.savefig("measurements/barplot_result2.pdf", format="pdf")
# plt.savefig("measurements/barplot_result2.png")
print("barplot_result2 generated")

#================ Test case 3 ================#
plt.figure() # different nb of patterns
res = sns.barplot(data=df_case3, x="NB_PATTERNS", y="Requests/sec", hue="Flag", palette=colors, edgecolor='black')
for i in res.containers: res.bar_label(i, fontsize=6.5)
plt.legend(title="Optimisation method")
plt.xlabel("Number of Patterns")
plt.ylabel("Requests/sec")
plt.title("Requests/sec by number of patterns for every optimisation method")
plt.savefig("measurements/barplot_result3.pdf", format="pdf")
# plt.savefig("measurements/barplot_result3.png")
print("barplot_result3 generated")




# List of input files and their labels
files = [
    ("measurements/test_case4_basic.csv", "Basic"),
    ("measurements/test_case4_cacheaware.csv", "Cache Aware"),
    ("measurements/test_case4_unroll.csv", "Unroll"),
    ("measurements/test_case4_best.csv", "Best")
]

# Data aggregation
data_frames = []

for dataset in files:
    df = pd.read_csv(dataset[0])
    df['Dataset'] = dataset[1]  # Update Dataset to label from files tuple
    
    # Calculate rates
    df['Branch Miss Rate'] = df[' (branch-misses)'] / df[' (branches)']
    df['L1 Miss Rate'] = df[' (L1-dcache-load-misses)'] / df[' (L1-dcache-loads)']
    df['Stalled Cycles'] = df[' (stalled-cycles-frontend)']
    
    data_frames.append(df)

# Combine all datasets
combined_df = pd.concat(data_frames)

# Aggregate the data for plotting with mean and standard deviation
metrics = ['Branch Miss Rate', 'L1 Miss Rate', 'Stalled Cycles']
plot_data = combined_df.groupby(['NB_WORKERS', 'Dataset'])[metrics].agg(['mean', 'std']).reset_index()

# Flatten MultiIndex columns
plot_data.columns = ['NB_WORKERS', 'Dataset'] + [
    f"{metric}_{agg}" for metric in metrics for agg in ['mean', 'std']
]

# Assign hue labels for seaborn
hue_order = [label for _, label in files]

# Colors for metrics
colors = ['red', 'orange', 'yellow', 'green']

# Plotting function
def plot_metric(data, metric, ylabel, filename):
    plt.figure(figsize=(10, 6))
    res = sns.barplot(
        data=data, 
        x='NB_WORKERS', 
        y=f'{metric}_mean', 
        hue='Dataset', 
        hue_order=hue_order, 
        palette=colors, 
        edgecolor='black',
        ci=None  # Disable seaborn's built-in error bars
    )
    
    # Add error bars manually
    for i, bar in enumerate(res.patches):
        group_idx = i % len(hue_order)  # Get corresponding group index
        nb_workers = data['NB_WORKERS'].iloc[i // len(hue_order)]
        dataset = hue_order[group_idx]
        std_dev = data.loc[
            (data['NB_WORKERS'] == nb_workers) & (data['Dataset'] == dataset),
            f'{metric}_std'
        ].values[0]
        # Add error bar
        bar_x = bar.get_x() + bar.get_width() / 2
        plt.errorbar(bar_x, bar.get_height(), yerr=std_dev, fmt='none', c='black', capsize=5)

    # Customize plot
    res.set_xlabel("Number of Workers")
    res.set_ylabel(ylabel)
    res.set_title(f"{ylabel} by Number of Workers for every optimisation method")
    plt.legend(title="Flag")
    plt.savefig(filename, format="pdf")

# Plot all metrics
plot_metric(plot_data, 'Branch Miss Rate', "Branch Miss Rate", "measurements/barplot_result5.pdf")
plot_metric(plot_data, 'L1 Miss Rate', "L1 Miss Rate", "measurements/barplot_result6.pdf")
plot_metric(plot_data, 'Stalled Cycles', "Stalled Cycles", "measurements/barplot_result7.pdf")



#================ Test case 4 ================#

# Load all the CSV file with pandas and add Worker
df_4_0_1 = pd.read_csv("measurements/test_case4_basic1.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_0_1 = df_4_0_1.assign(Worker = [1])
df_4_1_1 = pd.read_csv("measurements/test_case4_cache_aware1.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_1_1 = df_4_1_1.assign(Worker = [1])
df_4_2_1 = pd.read_csv("measurements/test_case4_unrolled1.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_2_1 = df_4_2_1.assign(Worker = [1])
df_4_3_1 = pd.read_csv("measurements/test_case4_best1.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_3_1 = df_4_3_1.assign(Worker = [1])

df_4_0_2 = pd.read_csv("measurements/test_case4_basic2.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_0_2 = df_4_0_2.assign(Worker = [2])
df_4_1_2 = pd.read_csv("measurements/test_case4_cache_aware2.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_1_2 = df_4_1_2.assign(Worker = [2])
df_4_2_2 = pd.read_csv("measurements/test_case4_unrolled2.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_2_2 = df_4_2_2.assign(Worker = [2])
df_4_3_2 = pd.read_csv("measurements/test_case4_best2.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_3_2 = df_4_3_2.assign(Worker = [2])

df_4_0_3 = pd.read_csv("measurements/test_case4_basic3.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_0_3 = df_4_0_3.assign(Worker = [4])
df_4_1_3 = pd.read_csv("measurements/test_case4_cache_aware3.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_1_3 = df_4_1_3.assign(Worker = [4])
df_4_2_3 = pd.read_csv("measurements/test_case4_unrolled3.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_2_3 = df_4_2_3.assign(Worker = [4])
df_4_3_3 = pd.read_csv("measurements/test_case4_best3.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_3_3 = df_4_3_3.assign(Worker = [4])

df_4_0_4 = pd.read_csv("measurements/test_case4_basic4.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_0_4 = df_4_0_4.assign(Worker = [8])
df_4_1_4 = pd.read_csv("measurements/test_case4_cache_aware4.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_1_4 = df_4_1_4.assign(Worker = [8])
df_4_2_4 = pd.read_csv("measurements/test_case4_unrolled4.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_2_4 = df_4_2_4.assign(Worker = [8])
df_4_3_4 = pd.read_csv("measurements/test_case4_best4.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_4_3_4 = df_4_3_4.assign(Worker = [8])

# add optimisation flags
df_basic4 = pd.concat([df_4_0_1, df_4_0_2, df_4_0_3, df_4_0_4], axis=0)
df_basic4 = df_basic4.assign(Flag = ["No optimisation"]*4)
df_cache_aware4 = pd.concat([df_4_1_1, df_4_1_2, df_4_1_3, df_4_1_4], axis=0)
df_cache_aware4 = df_cache_aware4.assign(Flag = ["Cache aware"]*4)
df_unrolled4 = pd.concat([df_4_2_1, df_4_2_2, df_4_2_3, df_4_2_4], axis=0)
df_unrolled4 = df_unrolled4.assign(Flag = ["Loop unrolling"]*4)
df_best4 = pd.concat([df_4_3_1, df_4_3_2, df_4_3_3, df_4_3_4], axis=0)
df_best4 = df_best4.assign(Flag = ["Best optimisation"]*4)

# all in one
df4 = pd.concat([df_basic4, df_cache_aware4, df_unrolled4, df_best4], axis=0)
# print(df4.to_string())

# barplot
plt.figure()
res = sns.barplot(data=df4, x="Worker", y="Requests/sec", hue="Flag", errorbar=None, palette=colors, edgecolor='black')
for i in res.containers: res.bar_label(i, fontsize=6.5)
plt.xlabel("Number of Workers")
plt.ylabel("Requests/sec")
plt.title("Requests/sec by number of workers for every optimisation method")
plt.savefig("measurements/barplot_result4.pdf", format="pdf")
# plt.savefig("measurements/barplot_result4.png")
print("barplot_result4 generated")


#================ PERF tests ================#



files = [
    ("measurements/test_case4_basic.csv", "Basic"),
    ("measurements/test_case4_cacheaware.csv", "Cache Aware"),
    ("measurements/test_case4_unroll.csv", "Unroll"),
    ("measurements/test_case4_best.csv", "Best")
]

data_frames = []

for dataset in files:
    df = pd.read_csv(dataset[0])
    df['Dataset'] = dataset[1] 
    
    # Calculate rates
    df['Branch Miss Rate'] = df[' (branch-misses)'] / df[' (branches)']
    df['L1 Miss Rate'] = df[' (L1-dcache-load-misses)'] / df[' (L1-dcache-loads)']
    df['Stalled Cycles'] = df[' (stalled-cycles-frontend)']
    
    data_frames.append(df)

combined_df = pd.concat(data_frames)

metrics = ['Branch Miss Rate', 'L1 Miss Rate', 'Stalled Cycles']
plot_data = combined_df.groupby(['NB_WORKERS', 'Dataset'])[metrics].agg(['mean', 'std']).reset_index()

plot_data.columns = ['NB_WORKERS', 'Dataset'] + [
    f"{metric}_{agg}" for metric in metrics for agg in ['mean', 'std']
]

# hue labels
hue_order = [label for _, label in files]

def plot_perf(data, metric, ylabel, filename):
    plt.figure(figsize=(10, 6))
    res = sns.barplot(
        data=data, 
        x='NB_WORKERS', 
        y=f'{metric}_mean', 
        hue='Dataset', 
        hue_order=hue_order, 
        palette=colors, 
        edgecolor='black',
        ci=None
    )
    
    # error bars
    for i, bar in enumerate(res.patches):
        group_idx = i % len(hue_order)  # Get corresponding group index
        nb_workers = data['NB_WORKERS'].iloc[i // len(hue_order)]
        dataset = hue_order[group_idx]
        std_dev = data.loc[
            (data['NB_WORKERS'] == nb_workers) & (data['Dataset'] == dataset),
            f'{metric}_std'
        ].values[0]
        bar_x = bar.get_x() + bar.get_width() / 2
        plt.errorbar(bar_x, bar.get_height(), yerr=std_dev, fmt='none', c='black', capsize=5)

    res.set_xlabel("Number of Workers")
    res.set_ylabel(ylabel)
    res.set_title(f"{ylabel} by Number of Workers for every optimisation method")
    plt.legend(title="Flag", loc='upper left') 
    plt.savefig(filename, format="pdf")

# Plot all metrics
plot_perf(plot_data, 'Branch Miss Rate', "Branch Miss Rate", "measurements/barplot_result5.pdf")
plot_perf(plot_data, 'L1 Miss Rate', "L1 Miss Rate", "measurements/barplot_result6.pdf")
plot_perf(plot_data, 'Stalled Cycles', "Stalled Cycles", "measurements/barplot_result7.pdf")



#^ =================== task 1_2_3 perf ===================



csv_directory = "./measurements"
file_patterns = [
    ("basic", "Basic"),
    ("cache_aware", "Cache Aware"),
    ("unrolled", "Unroll"),
    ("best", "Best"),
]

merged_frames = []
for method, optimization_method in file_patterns:
    for i in range(1, 4):
        file_name = f"test_case{i}_{method}.csv"
        file_path = os.path.join(csv_directory, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["TEST_CASE"] = str(i)
            df["Optimization_Method"] = optimization_method
            merged_frames.append(df)
        else:
            print(f"File not found: {file_path}")

merged_df = pd.concat(merged_frames, ignore_index=True)
output_file = os.path.join(csv_directory, "test_case_all_1_2_3.csv")
merged_df.to_csv(output_file, index=False)
print(f"Merged CSV saved as {output_file}")

df = pd.read_csv(output_file)
df.columns = df.columns.str.strip()
grouped_requests = df.groupby(['TEST_CASE', 'Optimization_Method'])['Requests/sec'].mean().reset_index()

files = [f"test_case1_2_3_{method}.csv" for method, _ in file_patterns]
performance_frames = []
for file, (_, optimization_method) in zip(files, file_patterns):
    file_path = os.path.join(csv_directory, file)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, comment='#')
        df['Optimization_Method'] = optimization_method

        df['Cycles/sec'] = df[' (cycles)'] / (df['task-clock (msec)'] / 1000)
        df['Instructions/sec'] = df[' (instructions)'] / (df['task-clock (msec)'] / 1000)
        performance_frames.append(df)
    else:
        print(f"File not found: {file_path}")

combined_performance = pd.concat(performance_frames)

grouped_performance = combined_performance.groupby(['TEST_CASE', 'Optimization_Method'])[
    ['Cycles/sec', 'Instructions/sec']
].mean().reset_index()

merged_df = pd.merge(grouped_performance, grouped_requests, on=['TEST_CASE', 'Optimization_Method'])

merged_df['Cycles/Request'] = merged_df['Cycles/sec'] / merged_df['Requests/sec']
merged_df['Instructions/Request'] = merged_df['Instructions/sec'] / merged_df['Requests/sec']


sns.set(style="whitegrid", context="talk", font_scale=1.2)

plt.figure(figsize=(12, 8))

hue_order = ['Basic', 'Cache Aware', 'Unroll', 'Best']
for i in range(2):
    for j in range(4):
        hue_order.append(hue_order[j])
        
barplot = sns.barplot(
    data=merged_df, 
    x='TEST_CASE', 
    y='Cycles/Request', 
    hue=hue_order, 
    palette=colors, 
    edgecolor='black'
)

barplot.set_xlabel('Test Case', fontsize=14)
barplot.set_ylabel('Cycles per Request', fontsize=14)
barplot.set_title('Cycles per Request by Test Case and Optimization Method', fontsize=16)
plt.legend(title="Flag", loc='upper left') 


plt.tight_layout()

plt.savefig("measurements/cycles_per_request.pdf", format="pdf")




files = [
    ("measurements/test_case1_2_3_basic.csv", "Basic"),
    ("measurements/test_case1_2_3_cache_aware.csv", "Cache Aware"),
    ("measurements/test_case1_2_3_unrolled.csv", "Unroll"),
    ("measurements/test_case1_2_3_best.csv", "Best"),
]

data_frames = []

for dataset in files:
    df = pd.read_csv(dataset[0], comment='#')
    df['Dataset'] = dataset[1]
    
    df['Branch Miss rate'] = (df[' (branch-misses)'] / df[' (instructions)']) * 100
    
    data_frames.append(df)

combined_df = pd.concat(data_frames)

plot_data = combined_df.groupby(['TEST_CASE', 'Dataset'])['Branch Miss rate'].agg(['mean', 'std']).reset_index()

plot_data.columns = ['TEST_CASE', 'Dataset', 'Branch Miss rate_mean', 'Branch Miss rate_std']

hue_order = [label for _, label in files]


def plot_metric(data, metric, ylabel, filename):
    plt.figure(figsize=(12, 8))
    res = sns.barplot(
        data=data, 
        x='TEST_CASE', 
        y=f'{metric}_mean', 
        hue='Dataset', 
        hue_order=hue_order, 
        palette=colors, 
        edgecolor='black',
        ci=None
    )
    
    for i, bar in enumerate(res.patches):
        group_idx = i % len(hue_order) 
        test_case = data['TEST_CASE'].iloc[i // len(hue_order)]
        dataset = hue_order[group_idx]
        std_dev = data.loc[
            (data['TEST_CASE'] == test_case) & (data['Dataset'] == dataset),
            f'{metric}_std'
        ].values[0]
        bar_x = bar.get_x() + bar.get_width() / 2
        plt.errorbar(bar_x, bar.get_height(), yerr=std_dev, fmt='none', c='black', capsize=5)

    res.set_xlabel("Test Case")
    res.set_ylabel(ylabel)
    res.set_title(f"{ylabel} by Test Case for every optimisation method")
    plt.legend(title="Flag")
    plt.savefig(filename, format="pdf")

plot_metric(plot_data, 'Branch Miss rate', "Branch Miss rate", "measurements/branch_misses_rate.pdf")


sns.set(style="whitegrid", context="talk", font_scale=1.2)

plt.figure(figsize=(12, 8))

hue_order = ['Basic', 'Cache Aware', 'Unroll', 'Best']
for i in range(2):
    for j in range(4):
        hue_order.append(hue_order[j])
 


instructions_plot = sns.barplot(
    data=merged_df, 
    x='TEST_CASE', 
    y='Instructions/Request', 
    hue=hue_order, 
    palette=colors, 
    edgecolor='black'
)

instructions_plot.set_xlabel('Test Case', fontsize=14)
instructions_plot.set_ylabel('Instructions per Request', fontsize=14)
instructions_plot.set_title('Instructions per Request by Test Case and Optimization Method', fontsize=16)
plt.legend(title="Flag", loc='upper left') 

plt.tight_layout()

plt.savefig("measurements/instructions_per_request.pdf", format="pdf")