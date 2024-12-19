USE gold_db
GO

-- =====================================================================================
-- Procedure Name: CreateSQLServerlessView_gold
-- Purpose: Dynamically creates or alters views in a Synapse Serverless database.
--          These views point to Delta Lake tables stored in an Azure Data Lake Storage
--          (ADLS) Gen2 container for easy access by Power BI or other reporting tools.
--
-- Parameters:
--     @ViewName (nvarchar(100)): The name of the view to be created or altered.
--
-- Functionality:
--     - Uses Synapse Serverless `OPENROWSET` to query Delta Lake files in ADLS Gen2.
--     - Dynamically constructs and executes a SQL statement to create or alter the view.
--
-- Usage:
--     EXEC CreateSQLServerlessView_gold @ViewName = 'MyTableName'
--
-- Assumptions:
--     - The Delta Lake folder for the table exists in the ADLS Gen2 storage at the specified path.
--     - The Synapse Serverless database has permissions to access the storage container.
--
-- =====================================================================================
CREATE OR ALTER PROC CreateSQLServerlessView_gold @ViewName nvarchar(100)
AS
BEGIN
    -- Declare a variable to hold the dynamic SQL statement.
    DECLARE @statement VARCHAR(MAX)

    -- Construct the dynamic SQL statement for creating or altering the view.
    SET @statement = N'CREATE OR ALTER VIEW ' + @ViewName + ' AS
        SELECT *
        FROM
            OPENROWSET(
                BULK ''https://dp207datalakegen2.dfs.core.windows.net/gold/SalesLT/' + @ViewName + '/'',
                FORMAT = ''DELTA''
            ) as [result]
    '

    -- Execute the dynamic SQL statement.
    EXEC (@statement)
END
GO
