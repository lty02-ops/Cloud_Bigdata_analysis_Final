from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, udf, explode, size, substring
from pyspark.sql.types import ArrayType, StringType, IntegerType
from itertools import combinations

spark = SparkSession.builder \
    .appName("CloudNativeStackCombinationAnalysis") \
    .master("local[*]") \
    .config("spark.eventLog.enabled", "false") \
    .getOrCreate()

df = spark.read.json(
    "file:///home/maria_dev/Cloud_Bigdata_Analysis/github_data/raw/*.json.gz"
)

df = df.select(
    col("type"),
    col("repo.name").alias("repo_name"),
    col("created_at")
).dropna()

df = df.withColumn("repo_lower", lower(col("repo_name")))
df = df.withColumn("year", substring(col("created_at"), 1, 4))

tech_keywords = [
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "helm",
    "terraform",
    "jenkins",
    "prometheus",
    "grafana"
]

def extract_techs(repo_name):
    found = []
    for tech in tech_keywords:
        if tech in repo_name:
            found.append(tech)
    return sorted(list(set(found)))

def make_combinations(techs):
    result = []
    for r in range(2, len(techs) + 1):
        for combo in combinations(techs, r):
            result.append("+".join(combo))
    return result

def combo_size(combo):
    return len(combo.split("+"))

extract_techs_udf = udf(extract_techs, ArrayType(StringType()))
make_combinations_udf = udf(make_combinations, ArrayType(StringType()))
combo_size_udf = udf(combo_size, IntegerType())

tech_df = df.withColumn("techs", extract_techs_udf(col("repo_lower")))

single_tech_df = tech_df.withColumn("technology", explode(col("techs")))

tech_count = single_tech_df.groupBy("technology").count() \
    .orderBy(col("count").desc())

combo_base = tech_df.filter(size(col("techs")) >= 2)

combo_df = combo_base.withColumn(
    "combination",
    explode(make_combinations_udf(col("techs")))
)

combo_df = combo_df.withColumn(
    "combo_size",
    combo_size_udf(col("combination"))
)

combo_count = combo_df.groupBy("combo_size", "combination").count() \
    .orderBy(col("combo_size"), col("count").desc())

print("===== Technology Activity Top 10 =====")
tech_count.show(10, False)

print("===== Pair Top 5 =====")
combo_count.filter(col("combo_size") == 2) \
    .orderBy(col("count").desc()) \
    .show(5, False)

print("===== Triple Top 5 =====")
combo_count.filter(col("combo_size") == 3) \
    .orderBy(col("count").desc()) \
    .show(5, False)

print("===== Four or More Combination Top 5 =====")
combo_count.filter(col("combo_size") >= 4) \
    .orderBy(col("count").desc()) \
    .show(5, False)

tech_count.coalesce(1).write.mode("overwrite").csv(
    "file:///home/maria_dev/Cloud_Bigdata_Analysis/output/technology_count",
    header=True
)

combo_count.coalesce(1).write.mode("overwrite").csv(
    "file:///home/maria_dev/Cloud_Bigdata_Analysis/output/combination_count",
    header=True
)

spark.stop()
