from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ExtractGithubForHive").master("local[*]").config("spark.eventLog.enabled", "false").getOrCreate()

df = spark.read.json("file:///home/maria_dev/Cloud_Bigdata_Analysis/github_data/raw/*.json.gz")

small_df = df.select(col("type"), col("repo.name").alias("repo_name"), col("created_at")).dropna()
small_df.coalesce(1).write.mode("overwrite").option("header", "true").csv("file:///home/maria_dev/Cloud_Bigdata_Analysis/output/github_events_small")
spark.stop()
