import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the CSV file with pandas
df = pd.read_csv("results.csv", sep=",", header=0, names=["MATSIZE", "PATTERNS_SIZE", "NB_PATTERNS", "THREADS", "CONNECTIONS", "RATE", "Requests/sec", "Transfer/sec"])
# turn into float to avoid errors
df["Transfer/sec"] = df["Transfer/sec"].str.replace("KB", "")
df["Transfer/sec"] = df["Transfer/sec"].str.replace("B", "")
# change Transfer/sec to float64
df["Transfer/sec"] = df["Transfer/sec"].astype(float)
# discard zeros in Requests/sec and Transfer/sec
df = df[~df.iloc[:, -1].astype(float).eq(0) & ~df.iloc[:, -2].astype(float).eq(0)]
# print(df)

plt.rcParams.update({"figure.max_open_warning": 0})
sns.set(style="darkgrid")
# parameters = ["MATSIZE", "PATTERNS_SIZE", "NB_PATTERNS", "THREADS", "CONNECTIONS", "RATE"]
# results = ["Requests/sec", "Transfer/sec"]


# most interesting plots for now :
# 1 heatmap
# 2 stripplot
# 3 jointplot
# 4 scatterplot
# 5 boxplot
# 6 pairplot


########## GENERAL ##########
# pairplot
plt.figure()
sns.pairplot(data=df, hue="RATE")
plt.savefig("measurements/pairplot.svg", format="svg")

# heatmap / correlation
plt.figure(figsize=(14, 12))
re = sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
re.set_xticklabels(re.get_xticklabels(), rotation=0)
re.set_yticklabels(re.get_yticklabels(), rotation=90)
plt.savefig("measurements/heatmap.svg", format="svg")



########## MATSIZE ##########
## Requests ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", size="PATTERNS_SIZE", palette="deep")
plt.xlabel("MATSIZE")
plt.ylabel("Requests/sec")
plt.legend(title="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_request_scatterplot.svg", format="svg")

# boxplot
plt.figure()
sns.boxplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_request_boxplot.svg", format="svg")

# stripplot
plt.figure()
sns.stripplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/MATSIZE_request_stripplot.svg", format="svg")

# jointplot
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_request_jointplot.svg", format="svg")



## Transfer ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS", size="PATTERNS_SIZE", palette="deep")
plt.xlabel("MATSIZE")
plt.ylabel("Transfer/sec")
plt.legend(title="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_transfer_scatterplot.svg", format="svg")

# boxplot
plt.figure()
sns.boxplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_transfer_boxplot.svg", format="svg")

# stripplot
plt.figure()
sns.stripplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/MATSIZE_transfer_stripplot.svg", format="svg")

# jointplot
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_transfer_jointplot.svg", format="svg")




########## PATTERNS_SIZE ##########
## Request ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS", size="MATSIZE", palette="deep")
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Requests/sec")
plt.legend(title="MATSIZE")
plt.savefig("measurements/PATTERNS_SIZE_request_scatterplot.svg", format="svg")

# boxplot
plt.figure()
sns.boxplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_request_boxplot.svg", format="svg")

# stripplot
plt.figure()
sns.stripplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/PATTERNS_SIZE_request_stripplot.svg", format="svg")

# jointplot
plt.figure()
sns.jointplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_request_jointplot.svg", format="svg")



## Transfer ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS", size="MATSIZE", palette="deep")
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Transfer/sec")
plt.legend(title="MATSIZE")
plt.savefig("measurements/PATTERNS_SIZE_transfer_scatterplot.svg", format="svg")

# boxplot
plt.figure()
sns.boxplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_transfer_boxplot.svg", format="svg")

# stripplot
plt.figure()
sns.stripplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/PATTERNS_SIZE_transfer_stripplot.svg", format="svg")

# jointplot
plt.figure()
sns.jointplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_transfer_jointplot.svg", format="svg")



