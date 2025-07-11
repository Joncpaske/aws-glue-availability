"""Pylint Conftest module for fixtures and helper functions"""

# pylint: disable=redefined-outer-name, unused-argument

import os

import boto3
import pytest
from moto import mock_aws


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""

    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"


@pytest.fixture(scope="function")
def glue_client(aws_credentials):
    """
    Mocked Boto Glue client with test aws creds
    """
    with mock_aws():
        yield boto3.client("glue")


@pytest.fixture(scope="function")
def ec2_client(aws_credentials):
    """
    Mocked Boto EC2 client with test aws creds
    """
    with mock_aws():
        yield boto3.client("ec2")
