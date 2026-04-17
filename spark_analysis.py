from pyspark.sql import SparkSession

# Start Spark
spark = SparkSession.builder \
    .appName("Cloud Monitoring Analysis") \
    .getOrCreate()

# Load CSV
df = spark.read.csv(
    "data/resource_metrics.csv",
    header=True,
    inferSchema=True
)

print("=== Raw Data ===")
df.show(5)

print("=== Average Usage ===")
df.selectExpr(
    "avg(cpu) as avg_cpu",
    "avg(ram) as avg_ram",
    "avg(disk) as avg_disk"
).show()

print("=== Peak Usage ===")
df.selectExpr(
    "max(cpu) as max_cpu",
    "max(ram) as max_ram",
    "max(disk) as max_disk"
).show()

spark.stop()