from databricks_library.tables import Table
from databricks_library.fixtures import Fixture

# my_table = Table("test_catalog ", "silver", "table_name")

# print(my_table.fully_qualified_table_name)

my_fix = Fixture()

print(my_fix.VALID_SCHEMAS)