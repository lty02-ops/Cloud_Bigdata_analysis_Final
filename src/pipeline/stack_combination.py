from itertools import combinations
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, udf, explode, size
from pyspark.sql.types import ArrayType, StringType, IntegerType

spark = SparkSession.builder.appName("CloudTechAnalysis").master("local[*]").config("spark.eventLog.enabled", "false").getOrCreate()

df = spark.read.json("file:///home/maria_dev/Cloud_Bigdata_Analysis/github_data/raw/*.json.gz")
df = df.select(col("type"), col("repo.name").alias("repo_name"), col("created_at")).dropna()
df = df.withColumn("repo_lower", lower(col("repo_name")))

keywords = ["aws", "azure", "gcp", "docker", "kubernetes", "helm", "terraform", "jenkins", "prometheus", "grafana"]

def find_keywords(repo_name):
    if repo_name is None:
        return []
    found = []
    for word in keywords:
        if word in repo_name:
            found.append(word)
    return list(set(found))

def make_combo(words):
    result = []
    for r in range(2, len(words) + 1):
        for combo in combinations(sorted(words), r):
            result.append("+".join(combo))
    return result

def count_size(combo):
    return len(combo.split("+"))

find_keywords_udf = udf(find_keywords, ArrayType(StringType()))
make_combo_udf = udf(make_combo, ArrayType(StringType()))
count_size_udf = udf(count_size, IntegerType())

repo_df = df.withColumn("techs", find_keywords_udf(col("repo_lower")))
activity_df = repo_df.withColumn("technology", explode(col("techs")))
activity_count = activity_df.groupBy("technology").count().orderBy(col("count").desc())

multi_repo = repo_df.filter(size(col("techs")) >= 2)
combination_df = multi_repo.withColumn("combination", explode(make_combo_udf(col("techs"))))
combination_df = combination_df.withColumn("combo_size", count_size_udf(col("combination")))
combination_count = combination_df.groupBy("combo_size", "combination").count().orderBy(col("combo_size"), col("count").desc())

print("technology count")
activity_count.show(10, False)

print("combo size 2")
combination_count.filter(col("combo_size") == 2).orderBy(col("count").desc()).show(5, False)

print("combo size 3")
combination_count.filter(col("combo_size") == 3).orderBy(col("count").desc()).show(5, False)

print("combo size >= 4")
combination_count.filter(col("combo_size") >= 4).orderBy(col("count").desc()).show(5, False)

activity_count.coalesce(1).write.mode("overwrite").csv("file:///home/maria_dev/Cloud_Bigdata_Analysis/output/technology_count")
combination_count.coalesce(1).write.mode("overwrite").csv("file:///home/maria_dev/Cloud_Bigdata_Analysis/output/combination_count")
spark.stop()
