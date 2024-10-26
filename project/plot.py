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

sns.set(style="darkgrid")

# parameters = ["MATSIZE", "PATTERNS_SIZE", "NB_PATTERNS", "THREADS", "CONNECTIONS", "RATE"]
# results = ["Requests/sec", "Transfer/sec"]
plot_bool = False


# most interesting plots for now :
# 1 heatmap
# 2 stripplot
# 3 jointplot (no reg)
# 4 scatterplot
# 5 boxplot
# 6 pairplot


###### GENERAL ######
# pairplot
plt.figure()
sns.pairplot(data=df, hue="RATE")
plt.savefig("measurements/pairplot.svg")
if plot_bool: plt.show()
# heatmap / correlation
plt.figure(figsize=(14, 12))
re = sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
re.set_xticklabels(re.get_xticklabels(), rotation=0)
re.set_yticklabels(re.get_yticklabels(), rotation=90)
plt.savefig("measurements/heatmap.svg")
if plot_bool: plt.show()

###### MATSIZE ######
# scatterplot
plt.figure()
sns.scatterplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", size="PATTERNS_SIZE", palette="deep")
plt.xlabel("MATSIZE")
plt.ylabel("Requests/sec")
plt.legend(title="NB_PATTERNS")
plt.savefig("measurements/scatterplot_MATSIZE.svg")
if plot_bool: plt.show()
# boxplot
plt.figure()
sns.boxplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/boxplot_MATSIZE.svg")
if plot_bool: plt.show()
# stripplot
plt.figure()
sns.stripplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS", dodge=True)
plt.savefig("measurements/stripplot_MATSIZE.svg")
if plot_bool: plt.show()
# jointplot
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Requests/sec", hue="NB_PATTERNS")
plt.savefig("measurements/jointplot_MATSIZE.svg")
if plot_bool: plt.show()
# jointplot with regression
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Requests/sec", kind="reg")
plt.savefig("measurements/jointplot_MATSIZE_regression.svg")
if plot_bool: plt.show()

