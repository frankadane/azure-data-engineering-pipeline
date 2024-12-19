# Databricks notebook source


## Transforming Bronze to Silver Tables
#  This script performs transformations on all tables in the "bronze" layer and writes the processed data to the "silver" layer in Delta format. The transformations include:
# a.- Adjusting date columns to a standard "yyyy-MM-dd" format.
# b.- Saving the transformed tables to their respective directories in the "silver" layer.


# Initialize an empty list to store table names.
table_name = []

# List all directories (tables) in the bronze layer's SalesLT folder.
# Append each table's name to the table_name list.
for i in dbutils.fs.ls('mnt/bronze/SalesLT/'):
    print(i.name)  # Print the name of each table directory for debugging.
    table_name.append(i.name.split('/')[0])  # Extract and store the directory name.


# Print the list of table names for verification.
table_name


from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

# Iterate through each table name to process and transform the data.
for i in table_name:
    # Define the path to the Parquet file in the bronze layer for the current table.
    path = '/mnt/bronze/SalesLT/' + i + '/' + i + '.parquet'
    
    # Read the Parquet file into a Spark DataFrame.
    df = spark.read.format('parquet').load(path)
    column = df.columns  # Get a list of column names in the DataFrame.

    # Iterate through columns to find and transform date fields.
    for col in column:
        if "Date" in col or "date" in col:  # Check for columns with "Date" in their name.
            # Convert UTC timestamps to "yyyy-MM-dd" format.
            df = df.withColumn(col, date_format(from_utc_timestamp(df[col].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))

    # Define the output path for the transformed table in the silver layer.
    output_path = '/mnt/silver/SalesLT/' + i + '/'
    
    # Write the transformed DataFrame to the silver layer in Delta format.
    df.write.format('delta').mode("overwrite").save(output_path)






