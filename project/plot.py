import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({"figure.max_open_warning": 0})
sns.set(style="darkgrid")

# Load all the CSV file with pandas
df_1_0 = pd.read_csv("test_case1_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_1 = pd.read_csv("test_case1_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_2 = pd.read_csv("test_case1_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_1_3 = pd.read_csv("test_case1_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])

df_2_0 = pd.read_csv("test_case2_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_1 = pd.read_csv("test_case2_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_2 = pd.read_csv("test_case2_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_2_3 = pd.read_csv("test_case2_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])

df_3_0 = pd.read_csv("test_case3_basic.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_1 = pd.read_csv("test_case3_cache_aware.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_2 = pd.read_csv("test_case3_unrolled.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])
df_3_3 = pd.read_csv("test_case3_best.csv", sep=",", header=0, names=["MATSIZE", "NB_PATTERNS", "PATTERNS_SIZE", "Requests/sec"])

print(df_1_0.to_string())
print(df_1_1.to_string())
print(df_1_2.to_string())
print(df_1_3.to_string())
print()
print(df_2_0.to_string())
print(df_2_1.to_string())
print(df_2_2.to_string())
print(df_2_3.to_string())
print()
print(df_3_0.to_string())
print(df_3_1.to_string())
print(df_3_2.to_string())
print(df_3_3.to_string())
print()


# TODO


"""

########## GENERAL ##########
# heatmap / correlation
plt.figure(figsize=(14, 12))
re = sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
re.set_xticklabels(re.get_xticklabels(), rotation=0)
re.set_yticklabels(re.get_yticklabels(), rotation=90)
plt.title("Correlation heatmap", y=1.02, fontsize = 26)
plt.savefig("measurements/heatmap.pdf", format="pdf")




########## MATSIZE ##########
## Requests ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="MATSIZE", y="Requests/sec", hue="PATTERNS_SIZE", palette="deep")
plt.ylim(0)
plt.xlabel("MATSIZE")
plt.ylabel("Requests/sec")
plt.title("Box plot of requests/sec by matrix and patterns sizes")
plt.savefig("measurements/MATSIZE_request_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="MATSIZE", y="Requests/sec", hue="PATTERNS_SIZE", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("MATSIZE")
plt.ylabel("Requests/sec")
plt.title("Strip plot of requests/sec by matrix and patterns sizes")
plt.savefig("measurements/MATSIZE_request_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Requests/sec", hue="PATTERNS_SIZE", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("MATSIZE")
plt.ylabel("Requests/sec")
plt.suptitle("Joint scatter plot of requests/sec by matrix and patterns sizes", fontsize=10)
plt.savefig("measurements/MATSIZE_request_jointplot.pdf", format="pdf")


## Transfer ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="MATSIZE", y="Transfer/sec", hue="PATTERNS_SIZE", palette="deep")
plt.ylim(0)
plt.xlabel("MATSIZE")
plt.ylabel("Transfer/sec [KB]")
plt.title("Box plot of transfer/sec by matrix and patterns sizes")
plt.savefig("measurements/MATSIZE_transfer_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="MATSIZE", y="Transfer/sec", hue="PATTERNS_SIZE", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("MATSIZE")
plt.ylabel("Transfer/sec [KB]")
plt.title("Strip plot of transfer/sec by matrix and patterns sizes")
plt.savefig("measurements/MATSIZE_transfer_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="MATSIZE", y="Transfer/sec", hue="PATTERNS_SIZE", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("MATSIZE")
plt.ylabel("Transfer/sec [KB]")
plt.suptitle("Joint scatter plot of transfer/sec by matrix and patterns sizes", fontsize=10)
plt.savefig("measurements/MATSIZE_transfer_jointplot.pdf", format="pdf")




########## PATTERNS_SIZE ##########
## Requests ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="MATSIZE", palette="deep")
plt.ylim(0)
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Requests/sec")
plt.title("Box plot of requests/sec by patterns and matrix sizes")
plt.savefig("measurements/PATTERNS_SIZE_request_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="MATSIZE", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Requests/sec")
plt.title("Strip plot of requests/sec by patterns and matrix sizes")
plt.savefig("measurements/PATTERNS_SIZE_request_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="PATTERNS_SIZE", y="Requests/sec", hue="MATSIZE", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Requests/sec")
plt.suptitle("Joint scatter plot of requests/sec by patterns and matrix sizes", fontsize=10)
plt.savefig("measurements/PATTERNS_SIZE_request_jointplot.pdf", format="pdf")


## Transfer ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="MATSIZE", palette="deep")
plt.ylim(0)
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Transfer/sec [KB]")
plt.title("Box plot of transfer/sec by patterns and matrix sizes")
plt.savefig("measurements/PATTERNS_SIZE_transfer_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="MATSIZE", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Transfer/sec [KB]")
plt.title("Strip plot of transfer/sec by patterns and matrix sizes")
plt.savefig("measurements/PATTERNS_SIZE_transfer_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="PATTERNS_SIZE", y="Transfer/sec", hue="MATSIZE", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("PATTERNS_SIZE")
plt.ylabel("Transfer/sec [KB]")
plt.suptitle("Joint scatter plot of transfer/sec by patterns and matrix sizes", fontsize=10)
plt.savefig("measurements/PATTERNS_SIZE_transfer_jointplot.pdf", format="pdf")




########## THREADS ##########
## Requests ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="THREADS", y="Requests/sec", hue="RATE", palette="deep")
plt.ylim(0)
plt.xlabel("THREADS")
plt.ylabel("Requests/sec")
plt.title("Box plot of requests/sec by number of threads and requests sent by second")
plt.savefig("measurements/THREADS_request_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="THREADS", y="Requests/sec", hue="RATE", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("THREADS")
plt.ylabel("Requests/sec")
plt.title("Strip plot of requests/sec by number of threads and requests sent by second")
plt.savefig("measurements/THREADS_request_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="THREADS", y="Requests/sec", hue="RATE", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("THREADS")
plt.ylabel("Requests/sec")
plt.suptitle("Joint scatter plot of requests/sec by number of threads and requests sent by second", fontsize=10)
plt.savefig("measurements/THREADS_request_jointplot.pdf", format="pdf")


## Transfer ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="THREADS", y="Transfer/sec", hue="RATE", palette="deep")
plt.ylim(0)
plt.xlabel("THREADS")
plt.ylabel("Transfer/sec [KB]")
plt.title("Box plot of transfer/sec by number of threads and requests sent by second")
plt.savefig("measurements/THREADS_transfer_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="THREADS", y="Transfer/sec", hue="RATE", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("THREADS")
plt.ylabel("Transfer/sec [KB]")
plt.title("Strip plot of transfer/sec by number of threads and requests sent by second")
plt.savefig("measurements/THREADS_transfer_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="THREADS", y="Transfer/sec", hue="RATE", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("THREADS")
plt.ylabel("Transfer/sec [KB]")
plt.suptitle("Joint scatter plot of transfer/sec by number of threads and requests sent by second", fontsize=10)
plt.savefig("measurements/THREADS_transfer_jointplot.pdf", format="pdf")




########## RATE ##########
## Requests ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="RATE", y="Requests/sec", hue="THREADS", palette="deep")
plt.ylim(0)
plt.xlabel("RATE")
plt.ylabel("Requests/sec")
plt.title("Box plot of requests/sec by number of requests sent by second and threads")
plt.savefig("measurements/RATE_request_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="RATE", y="Requests/sec", hue="THREADS", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("RATE")
plt.ylabel("Requests/sec")
plt.title("Strip plot of requests/sec by number of requests sent by second and threads")
plt.savefig("measurements/RATE_request_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="RATE", y="Requests/sec", hue="THREADS", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("RATE")
plt.ylabel("Requests/sec")
plt.suptitle("Joint scatter plot of requests/sec by number of requests sent by second and threads", fontsize=10)
plt.savefig("measurements/RATE_request_jointplot.pdf", format="pdf")


## Transfer ##
# boxplot
plt.figure()
sns.boxplot(data=df, x="RATE", y="Transfer/sec", hue="THREADS", palette="deep")
plt.ylim(0)
plt.xlabel("RATE")
plt.ylabel("Transfer/sec [KB]")
plt.title("Box plot of transfer/sec by number of requests sent by second and threads")
plt.savefig("measurements/RATE_transfer_boxplot.pdf", format="pdf")

# stripplot
plt.figure()
sns.stripplot(data=df, x="RATE", y="Transfer/sec", hue="THREADS", dodge=True, palette="deep")
plt.ylim(0)
plt.xlabel("RATE")
plt.ylabel("Transfer/sec [KB]")
plt.title("Strip plot of transfer/sec by number of requests sent by second and threads")
plt.savefig("measurements/RATE_transfer_stripplot.pdf", format="pdf")

# jointplot
plt.figure()
sns.jointplot(data=df, x="RATE", y="Transfer/sec", hue="THREADS", palette="deep")
plt.xlim(0)
plt.ylim(0)
plt.xlabel("RATE")
plt.ylabel("Transfer/sec [KB]")
plt.suptitle("Joint scatter plot of transfer/sec by number of requests sent by second and threads", fontsize=10)
plt.savefig("measurements/RATE_transfer_jointplot.pdf", format="pdf")

"""
