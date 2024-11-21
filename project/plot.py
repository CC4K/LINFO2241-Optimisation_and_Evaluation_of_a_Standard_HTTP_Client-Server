import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({"figure.max_open_warning": 0})
sns.set_theme(style="darkgrid")


#============= Test case 1, 2, 3 =============#

# Load all the CSV file with pandas and add test case numbers
df_1_0 = pd.read_csv("measurements/test_case1_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_0 = df_1_0.assign(Case = [1]*2)
df_1_1 = pd.read_csv("measurements/test_case1_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_1 = df_1_1.assign(Case = [1]*2)
df_1_2 = pd.read_csv("measurements/test_case1_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_2 = df_1_2.assign(Case = [1]*2)
df_1_3 = pd.read_csv("measurements/test_case1_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_3 = df_1_3.assign(Case = [1]*2)

df_2_0 = pd.read_csv("measurements/test_case2_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_0 = df_2_0.assign(Case = [2]*2)
df_2_1 = pd.read_csv("measurements/test_case2_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_1 = df_2_1.assign(Case = [2]*2)
df_2_2 = pd.read_csv("measurements/test_case2_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_2 = df_2_2.assign(Case = [2]*2)
df_2_3 = pd.read_csv("measurements/test_case2_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_3 = df_2_3.assign(Case = [2]*2)

df_3_0 = pd.read_csv("measurements/test_case3_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_0 = df_3_0.assign(Case = [3]*2)
df_3_1 = pd.read_csv("measurements/test_case3_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_1 = df_3_1.assign(Case = [3]*2)
df_3_2 = pd.read_csv("measurements/test_case3_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_2 = df_3_2.assign(Case = [3]*2)
df_3_3 = pd.read_csv("measurements/test_case3_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_3 = df_3_3.assign(Case = [3]*2)

# add optimisation flags
df_basic = pd.concat([df_1_0, df_2_0, df_3_0], axis=0)
df_basic = df_basic.assign(Flag = ["No optimisation"]*6)
df_cache_aware = pd.concat([df_1_1, df_2_1, df_3_1], axis=0)
df_cache_aware = df_cache_aware.assign(Flag = ["Cache aware"]*6)
df_unrolled = pd.concat([df_1_2, df_2_2, df_3_2], axis=0)
df_unrolled = df_unrolled.assign(Flag = ["Loop unrolling"]*6)
df_best = pd.concat([df_1_3, df_2_3, df_3_3], axis=0)
df_best = df_best.assign(Flag = ["Best optimisation"]*6)

# all in one
df = pd.concat([df_basic, df_cache_aware, df_unrolled, df_best], axis=0)
# print(df.to_string())

# barplot
plt.figure()
colors = ['red', 'orange', 'yellow', 'green']
sns.barplot(data=df, x="Case", y="Requests/sec", hue="Flag", errorbar=None, palette=colors)
plt.ylim(0)
plt.xlabel("Test case")
plt.ylabel("Requests/sec")
plt.title("Bar plot of Requests/sec by test case and optimisation method")
plt.savefig("measurements/barplot_result_1_2_3.pdf", format="pdf")
print("barplot_result_1_2_3 generated")



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
colors = ['red', 'orange', 'yellow', 'green']
sns.barplot(data=df4, x="Worker", y="Requests/sec", hue="Flag", errorbar=None, palette=colors)
plt.ylim(0)
plt.xlabel("Number of Workers")
plt.ylabel("Requests/sec")
plt.title("Bar plot of Requests/sec by # of workers and optimisation method")
plt.savefig("measurements/barplot_result4.pdf", format="pdf")
print("barplot_result4 generated")
