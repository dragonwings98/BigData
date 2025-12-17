# Import required modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, desc

# ======================
# 1. Initialize SparkSession (Core Entry Point)
# ======================
spark = SparkSession.builder \
    .appName("SparkCompleteDemo") \
    .master("local[*]") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Disable verbose logs to reduce output clutter
spark.sparkContext.setLogLevel("WARN")

print("===== Spark Environment Initialized Successfully =====")
print(f"Spark Version: {spark.version}")
print(f"Python Version: {spark.sparkContext.pythonVer}")

# ======================
# 2. Example 1: Basic RDD Operations (Word Count)
# ======================
print("\n===== Example 1: RDD Word Count =====")
# Test text data
text_data = [
    "Spark is a big data framework",
    "Spark supports RDD and DataFrame",
    "Python is easy to use with Spark",
    "Docker + Spark = portable big data"
]
# Parallelize data to create RDD
text_rdd = spark.sparkContext.parallelize(text_data)

# Core word count logic
word_count_rdd = text_rdd \
    .flatMap(lambda line: line.lower().split()) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)              # Aggregate counts by word

# Sort results by count (descending) and print
sorted_word_count = word_count_rdd.sortBy(lambda x: x[1], ascending=False).collect()
for word, count_val in sorted_word_count:
    print(f"Word: {word:10} Count: {count_val}")

# ======================
# 3. Example 2: DataFrame Operations (Sales Data Analysis)
# ======================
print("\n===== Example 2: DataFrame Sales Data Analysis =====")
# Simulated sales dataset
sales_data = [
    ("2025-12-01", "Beijing", "Electronics", 1500),
    ("2025-12-01", "Shanghai", "Clothing", 800),
    ("2025-12-02", "Beijing", "Electronics", 2000),
    ("2025-12-02", "Shanghai", "Electronics", 1200),
    ("2025-12-03", "Guangzhou", "Food", 500),
    ("2025-12-03", "Beijing", "Clothing", 600),
    ("2025-12-04", "Guangzhou", "Electronics", 1800)
]
# Create DataFrame with specified column names
sales_df = spark.createDataFrame(sales_data, ["date", "city", "category", "amount"])

# 3.1 Basic query: Print schema and first 5 rows
sales_df.printSchema()
print("Original Sales Data:")
sales_df.show(5)

# 3.2 Data filtering: Select Beijing's electronics sales records
beijing_electronics = sales_df.filter(
    (col("city") == "Beijing") & (col("category") == "Electronics")
)
print("\nBeijing Electronics Sales Records:")
beijing_electronics.show()

# 3.3 Aggregation analysis: Calculate total sales and order count by city
city_sales = sales_df.groupBy("city") \
    .agg(
        sum("amount").alias("total_sales"),
        count("date").alias("order_count")
    ) \
    .orderBy(desc("total_sales"))
print("\nCity Sales Summary (Sorted by Total Sales Descending):")
city_sales.show()

# ======================
# 4. Example 3: Spark SQL Operations
# ======================
print("\n===== Example 3: Spark SQL Analysis =====")
# Create a temporary view for SQL queries
sales_df.createOrReplaceTempView("sales_view")

# Execute SQL: Query records with sales amount > 1000
high_sales_sql = """
SELECT date, city, category, amount 
FROM sales_view 
WHERE amount > 1000
ORDER BY amount DESC
"""
high_sales_df = spark.sql(high_sales_sql)
print("Sales Records with Amount > 1000 (SQL Query):")
high_sales_df.show()

# ======================
# 5. Clean Up Resources
# ======================
spark.stop()
print("\n===== Spark Application Execution Completed =====")