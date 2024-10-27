import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the CSV file with pandas
df = pd.read_csv("results.csv", sep=",", header=0, names=["MATSIZE", "PATTERNS_SIZE", "NB_PATTERNS", "THREADS", "CONNECTIONS", "RATE", "Requests/sec", "Transfer/sec"])

def convert_transfer_rate(value):
    if 'MB' in value:
        return float(value.replace('MB', '')) * 1_000_000
    elif 'KB' in value:
        return float(value.replace('KB', '')) * 1_000
    elif 'B' in value:
        return float(value.replace('B', ''))
    else:
        return float(value)

df["Transfer/sec"] = df["Transfer/sec"].apply(convert_transfer_rate)

# discard 0 & -1 in Requests/sec and Transfer/sec
df = df[~df.iloc[:, -1].astype(float).eq(0) & ~df.iloc[:, -2].astype(float).eq(0) & ~df.iloc[:, -1].astype(float).eq(-1) & ~df.iloc[:, -2].astype(float).eq(-1)]
# print(df)

plt.rcParams.update({"figure.max_open_warning": 0})
sns.set(style="darkgrid")
# parameters = ["MATSIZE", "PATTERNS_SIZE", "NB_PATTERNS", "THREADS", "CONNECTIONS", "RATE"]
# results = ["Requests/sec", "Transfer/sec"]



########## GENERAL ##########
# pairplot
plt.figure()
sns.pairplot(data=df, hue="RATE")
plt.savefig("measurements/pairplot.pdf", format="pdf")

# heatmap / correlation
plt.figure(figsize=(14, 12))
re = sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
re.set_xticklabels(re.get_xticklabels(), rotation=0)
re.set_yticklabels(re.get_yticklabels(), rotation=90)
plt.savefig("measurements/heatmap.pdf", format="pdf")



########## MATSIZE ##########
## Requests ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", size="PATTERNS_SIZE", palette="deep")
plt.xlabel("MATSIZE")
plt.ylabel("Requests/sec")
plt.legend(title="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_request_scatterplot.pdf", format="pdf")

# boxplot
plt.figure()
sns.boxplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_request_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/MATSIZE_request_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_request_jointplot.pdf", format="pdf")


## Transfer ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS", size="PATTERNS_SIZE", palette="deep")
plt.xlabel("MATSIZE")
plt.ylabel("Transfer/sec")
plt.legend(title="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_transfer_scatterplot.pdf", format="pdf")

# boxplot
plt.figure()
sns.boxplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_transfer_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/MATSIZE_transfer_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/MATSIZE_transfer_jointplot.pdf", format="pdf")




########## PATTERNS_SIZE ##########
## Request ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS", size="MATSIZE", palette="deep")
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Requests/sec")
plt.legend(title="MATSIZE")
plt.savefig("measurements/PATTERNS_SIZE_request_scatterplot.pdf", format="pdf")

# boxplot
plt.figure()
sns.boxplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_request_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/PATTERNS_SIZE_request_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_request_jointplot.pdf", format="pdf")


## Transfer ##
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS", size="MATSIZE", palette="deep")
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Transfer/sec")
plt.legend(title="MATSIZE")
plt.savefig("measurements/PATTERNS_SIZE_transfer_scatterplot.pdf", format="pdf")

# boxplot
plt.figure()
sns.boxplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_transfer_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/PATTERNS_SIZE_transfer_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="NB_PATTERNS")
plt.savefig("measurements/PATTERNS_SIZE_transfer_jointplot.pdf", format="pdf")