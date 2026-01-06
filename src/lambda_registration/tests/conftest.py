import os
import pytest

@pytest.fixture(autouse=True)
def set_env():
    os.environ["DB_SECRET_NAME"] = "fake_secret_for_test"

    import os
import json
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def set_env():
    os.environ["DB_SECRET_NAME"] = "fake_secret_for_test"

@pytest.fixture
def mock_db_dependencies():
    with patch("lambda_registration.utils.db_client.boto3.client") as mock_boto, \
         patch("lambda_registration.utils.db_client.psycopg2.connect") as mock_connect:

        sm_instance = MagicMock()
        sm_instance.get_secret_value.return_value = {
            "SecretString": json.dumps({
                "host": "localhost",
                "username": "user",
                "password": "pass",
                "dbname": "testdb"
            })
        }
        mock_boto.return_value = sm_instance

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        yield mock_conn