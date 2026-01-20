import pytest
from unittest.mock import patch, MagicMock
import json
import os

import psycopg2
from utils.db_client import DBClient

@pytest.fixture
def fake_secret():
    return {
        "host": "localhost",
        "username": "user",
        "password": "pass",
        "dbname": "testdb"
    }

@patch("utils.db_client.boto3.client")
@patch("utils.db_client.psycopg2.connect")
def test_dbclient_init(mock_connect, mock_boto_client, fake_secret):
    sm_instance = MagicMock()
    sm_instance.get_secret_value.return_value = {"SecretString": json.dumps(fake_secret)}
    mock_boto_client.return_value = sm_instance

    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn

    os.environ["DB_SECRET_NAME"] = "fake_secret"
    client = DBClient()

    mock_boto_client.assert_called_once_with("secretsmanager", region_name="us-east-1")
    sm_instance.get_secret_value.assert_called_once_with(SecretId="fake_secret")
    mock_connect.assert_called_once()
    assert client._conn == mock_conn

@patch("utils.db_client.psycopg2.connect")
def test_dbclient_execute(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    os.environ["DB_SECRET_NAME"] = "fake_secret"
    with patch("utils.db_client.boto3.client") as mock_boto:
        sm_instance = MagicMock()
        sm_instance.get_secret_value.return_value = {"SecretString": json.dumps({'host':'h','username':'u','password':'p','dbname':'d'})}
        mock_boto.return_value = sm_instance
        client = DBClient()

    client.execute("SELECT 1", (1,))
    mock_cursor.execute.assert_called_once_with("SELECT 1", (1,))
    mock_conn.commit.assert_called_once()
