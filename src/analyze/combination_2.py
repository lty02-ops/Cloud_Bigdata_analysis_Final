import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../../results/combination_count.csv", header=None, names=["combo_size", "combination", "cnt"])

top5 = (df[df["combo_size"] == 2].sort_values("cnt", ascending=False).head(5))

plt.figure(figsize=(10,5))
plt.bar(top5["combination"], top5["cnt"])
plt.title("combination_2")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../../results/combo_size2_top5.png")
plt.show()
