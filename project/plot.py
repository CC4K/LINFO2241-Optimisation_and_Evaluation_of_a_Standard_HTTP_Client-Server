import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({"figure.max_open_warning": 0})
sns.set_theme(style="darkgrid")


# df_1_0 = pd.read_csv("measurements/test_case1_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
# df_1_0 = df_1_0.assign(Flag = ["No optimisation"]*2)
# df_1_1 = pd.read_csv("measurements/test_case1_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
# df_1_1 = df_1_1.assign(Flag = ["Cache awareness"]*2)
# df_1_2 = pd.read_csv("measurements/test_case1_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
# df_1_2 = df_1_2.assign(Flag = ["Loop unrolling"]*2)
# df_1_3 = pd.read_csv("measurements/test_case1_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
# df_1_3 = df_1_3.assign(Flag = ["Best optimisation"]*2)

# df_case1 = pd.concat([df_1_0, df_1_1, df_1_2, df_1_3], axis=0)
# df_case2 = pd.concat([df_2_0, df_2_1, df_2_2, df_2_3], axis=0)
# df_case3 = pd.concat([df_3_0, df_3_1, df_3_2, df_3_3], axis=0)
# print(df_case1.to_string())
# print(df_case2.to_string())
# print(df_case3.to_string())

colors = ['red', 'orange', 'yellow', 'green']


# plt.figure()
# res = sns.barplot(data=df_case1, x="MATSIZE", y="Requests/sec", hue="Flag", palette=colors, edgecolor='black')
# for i in res.containers: res.bar_label(i, fontsize=6.5)
# plt.legend(title="Optimisation method")
# plt.xlabel("Matrix Sizes")
# plt.ylabel("Requests/sec")
# plt.title("Requests/sec by matrix sizes for every optimisation method (log scale)")
# plt.yscale('log')
#
# plt.savefig("measurements/barplot_result1.pdf", format="pdf")
# # plt.savefig("measurements/barplot_result1.png")
# print("barplot_result1 generated")

