import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv("../../results/combination_count.csv")

top5 = (df[df["combo_size"] >= 4].sort_values("count", ascending=False).head(5))

plt.figure(figsize=(10,5))
plt.bar(top5["combination"], top5["count"])
plt.title("combination >=_4")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../../results/combo_size4plus_top5.png")
plt.show()
