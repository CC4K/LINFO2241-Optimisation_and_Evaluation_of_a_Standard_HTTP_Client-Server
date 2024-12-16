import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({"figure.max_open_warning": 0})
sns.set_theme(style="darkgrid")

df = pd.read_csv("SIMD.csv", sep=",", header=0, names=["CFLAG", "Requests/sec"])
# print(df.to_string())

plt.figure(figsize=(7, 6))
res = sns.barplot(data=df, x="CFLAG", y="Requests/sec", edgecolor="black")
for i in res.containers: res.bar_label(i, fontsize=11, padding=-25)
plt.xlabel("Method of optimisation")
plt.ylabel("Requests/sec")
plt.title("Requests/sec for every optimisation method")
plt.savefig("graph.png")
