import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv("results/combination_count.csv")

top10 = df.sort_values("count", ascending=False).head(10)

plt.figure(figsize=(10,5))
plt.bar(top10["combination"], top10["count"])
plt.title("All combination")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("results/all_combination_top10.png")
plt.show()
