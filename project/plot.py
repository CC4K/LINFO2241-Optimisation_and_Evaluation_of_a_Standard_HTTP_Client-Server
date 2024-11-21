import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({"figure.max_open_warning": 0})
sns.set(style="darkgrid")

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
plt.savefig("measurements/barplot_result.pdf", format="pdf")
