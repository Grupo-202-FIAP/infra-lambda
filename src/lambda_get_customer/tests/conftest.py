import os
import pytest

@pytest.fixture(autouse=True)
def set_env():
    os.environ["DB_HOST"] = "localhost:5432"
    os.environ["DB_USER"] = "testuser"
    os.environ["DB_PASSWORD"] = "testpass"
    os.environ["DB_NAME"] = "testdb"
    os.environ["CUSTOMER_TABLE"] = "customers"
