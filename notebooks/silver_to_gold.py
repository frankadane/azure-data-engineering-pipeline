# Databricks notebook source

# %md
# ## Transforming Silver to Gold Tables
# This script processes all tables in the "silver" layer and writes the transformed data to the "gold" layer. The transformation includes:
#  - Renaming column names to follow the `snake_case` naming convention.
#  - Saving the transformed tables in Delta format in the "gold" layer.



# Initialize an empty list to store table names.
table_name = []

# List all directories (tables) in the silver layer's SalesLT folder.
# Append each table's name to the table_name list.
for i in dbutils.fs.ls('mnt/silver/SalesLT/'):
    print(i.name)  # Print the name of each table directory for debugging.
    table_name.append(i.name.split('/')[0])  # Extract and store the directory name.



# Iterate through each table name to process and transform the data.
for name in table_name:
    # Define the path to the Delta table in the silver layer for the current table.
    path = '/mnt/silver/SalesLT/' + name
    print(path)  # Print the path for debugging.

    # Read the Delta table into a Spark DataFrame.
    df = spark.read.format('delta').load(path)

    # Get the list of column names.
    column_names = df.columns

    # Transform column names to snake_case format.
    for old_col_name in column_names:
        # Convert "ColumnName" to "column_name" using list comprehension.
        new_col_name = "".join([
            "_" + char if char.isupper() and (i > 0 and not old_col_name[i - 1].isupper()) else char
            for i, char in enumerate(old_col_name)
        ]).lstrip("_")  # Remove leading underscores if present.

        # Rename the column in the DataFrame.
        df = df.withColumnRenamed(old_col_name, new_col_name)

    # Define the output path for the transformed table in the gold layer.
    output_path = '/mnt/gold/SalesLT/' + name + '/'

    # Write the transformed DataFrame to the gold layer in Delta format.
    df.write.format('delta').mode("overwrite").save(output_path)



