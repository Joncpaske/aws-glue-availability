"""mocked e2e tests"""

from test.unit.helper import create_connections, create_jobs

from awsglueavailability import app
from awsglueavailability.client import EC2, Glue


def test_diagram(glue_client, ec2_client):
    """e2e test but does not validate diagram output"""

    job_names = ["glue_job_1", "glue_job_2"]

    vpc = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]
    subnet = ec2_client.create_subnet(VpcId=vpc["VpcId"], CidrBlock="10.0.1.0/24")[
        "Subnet"
    ]
    subnet1 = ec2_client.create_subnet(VpcId=vpc["VpcId"], CidrBlock="10.0.2.0/24")[
        "Subnet"
    ]

    create_connections(glue_client, ["glue_job_1_conn"], subnet["SubnetId"])
    create_connections(glue_client, ["glue_job_2_conn"], subnet1["SubnetId"])
    create_jobs(
        glue_client,
        job_names,
        [["glue_job_1_conn"], ["glue_job_1_conn", "glue_job_2_conn"]],
    )

    glue = Glue(glue_client)
    ec2 = EC2(ec2_client)

    app.draw_diagram(glue, ec2)
