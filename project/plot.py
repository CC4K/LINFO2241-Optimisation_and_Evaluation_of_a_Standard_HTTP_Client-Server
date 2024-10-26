import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the CSV file with pandas
df = pd.read_csv("results2.csv", sep=",", header=0, names=["MATSIZE", "PATTERNS_SIZE", "NB_PATTERNS", "THREADS", "CONNECTIONS", "RATE", "Requests/sec", "Transfer/sec"])
df["Transfer/sec"] = df["Transfer/sec"].str.replace("KB", "")
df["Transfer/sec"] = df["Transfer/sec"].str.replace("B", "")
# print(df)

sns.set(style="darkgrid")

# parameters = ["MATSIZE", "PATTERNS_SIZE", "NB_PATTERNS", "THREADS", "CONNECTIONS", "RATE"]
# results = ["Requests/sec", "Transfer/sec"]

# Alright I've been thinking, when life give you lemons, don"t make lemonade, make life take the lemons back! Get mad!I don"t want your damn lemons what am I supposed to do with these? Demand to see life"s manager! Make life rue the day it thought it could give Cédric Kheirallah lemons! Do you know who I am? I"m the man who"s gonna scatter your graph down! With the scattergraph! I"m gonna get my 3 last braincells to find a seaborn method that scatters your graph down!
# Just kidding : scattergraph & heatmap with all data at the same time ???? EZ with seaborn (I think)





# most interesting plots for now :
# 1 heatmap
# 2 stripplot
# 3 jointplot (no reg)
# 4 scatterplot
# 5 boxplot
# 6 pairplot


###### GENERAL ######
# pairplot
sns.pairplot(data=df, hue="RATE")
plt.show()
# plt.savefig("pairplot.png")
# heatmap / correlation
plt.figure(figsize=(14, 12))
re = sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
re.set_xticklabels(re.get_xticklabels(), rotation=0)
re.set_yticklabels(re.get_yticklabels(), rotation=90)
plt.show()
# plt.savefig("heatmap.png")

###### MATSIZE ######
# scatterplot
sns.scatterplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", size="PATTERNS_SIZE", palette="deep")
plt.xlabel("MATSIZE")
plt.ylabel("Requests/sec")
plt.legend(title="NB_PATTERNS")
plt.show()
# plt.savefig("scatterplot_MATSIZE.png")
# boxplot
sns.boxplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.show()
# plt.savefig("boxplot_MATSIZE.png")
# stripplot
sns.stripplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", dodge=True)
plt.show()
# plt.savefig("stripplot_MATSIZE.png")
# jointplot
sns.jointplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.show()
# plt.savefig("jointplot_MATSIZE.png")
sns.jointplot(data=df, x="MATSIZE", y="Requests/sec", kind="reg")
plt.show()
# plt.savefig("jointplot_MATSIZE_regression.png")

