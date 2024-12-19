# Databricks notebook source

# Configuration for mounting Azure Data Lake Storage (ADLS) Gen2
# The script uses Azure AD passthrough authentication to mount different layers (bronze, silver, gold) in Databricks.


# Configuration dictionary for Azure AD passthrough authentication.
configs = {
    "fs.azure.account.auth.type": "CustomAccessToken",
    "fs.azure.account.custom.token.provider.class": spark.conf.get(
        "spark.databricks.passthrough.adls.gen2.tokenProviderClassName"
    )
}

# Mount the "bronze" layer of the ADLS Gen2 storage.
# Replace <directory-name> in the source URI if a sub-directory needs to be mounted.
dbutils.fs.mount(
    source="abfss://bronze@dp207datalakegen2.dfs.core.windows.net/",
    mount_point="/mnt/bronze",
    extra_configs=configs
)

# Verify the mounted "bronze" layer by listing its contents.
dbutils.fs.ls("/mnt/bronze/SalesLT/")


# Reusing the same configuration to mount the "silver" layer.
configs = {
    "fs.azure.account.auth.type": "CustomAccessToken",
    "fs.azure.account.custom.token.provider.class": spark.conf.get(
        "spark.databricks.passthrough.adls.gen2.tokenProviderClassName"
    )
}

# Mount the "silver" layer of the ADLS Gen2 storage.
dbutils.fs.mount(
    source="abfss://silver@dp207datalakegen2.dfs.core.windows.net/",
    mount_point="/mnt/silver",
    extra_configs=configs
)


# Reusing the same configuration to mount the "gold" layer.
configs = {
    "fs.azure.account.auth.type": "CustomAccessToken",
    "fs.azure.account.custom.token.provider.class": spark.conf.get(
        "spark.databricks.passthrough.adls.gen2.tokenProviderClassName"
    )
}

# Mount the "gold" layer of the ADLS Gen2 storage.
dbutils.fs.mount(
    source="abfss://gold@dp207datalakegen2.dfs.core.windows.net/",
    mount_point="/mnt/gold",
    extra_configs=configs
)

