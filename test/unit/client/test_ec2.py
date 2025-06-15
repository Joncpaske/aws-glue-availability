"""Tests for boto EC2 client wrapper"""

from awsglueavailability.client import EC2, Subnet


def test_get_subnet(ec2_client):
    """test (happy path) retrieval of subnet associated to Glue connector"""

    # setup
    vpc = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]
    subnet = ec2_client.create_subnet(VpcId=vpc["VpcId"], CidrBlock="10.0.1.0/24")[
        "Subnet"
    ]

    ec2 = EC2(ec2_client)

    expected_result = Subnet(vpc=vpc["VpcId"], cidr_block="10.0.1.0/24")

    actual_result = ec2.get_subnet(subnet["SubnetId"])

    assert expected_result == actual_result, "subnet information incorrect"
