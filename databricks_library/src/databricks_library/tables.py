# from databricks_library._fixture import Fixture
from ._fixture import Fixture


class Table:

    def __init__(self, catalog: str, schema: str, name: str):
        assert catalog in Fixture.VALID_CATALOGS, f"{catalog} is not a valid catalog"
        self.catalog = catalog

        assert schema in Fixture.VALID_SCHEMAS, f"{schema} is not a valid schema"
        self.schema = schema
        self.name = name

        self.fully_qualified_table_name = f"{self.catalog}.{self.schema}.{self.name}"

if __name__ == "__main__":
    my_table = Table("test_catalog", "silver", "test")
    print(my_table.fully_qualified_table_name)