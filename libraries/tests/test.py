from databricks.table import Table

print(Table("test_catalog", "silver", "test").fully_qualified_table_name)