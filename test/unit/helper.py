"""helper methods for creating AWS resources for test prepperation"""


def create_job(glue_client, name: str, conns: list[str] = None) -> None:
    """Create default base Glue Job"""

    job_definition = {
        "Name": name,
        "Description": f"{name} - description",
        "Role": f"arn:aws:iam:::role/{name}",
        "Command": {
            "Name": "glueetl",
            "ScriptLocation": "my/scriptl/ocation",
            "PythonVersion": "3",
        },
        "GlueVersion": "3.0",
    }

    if conns:
        job_definition["Connections"] = {"Connections": conns}

    glue_client.create_job(**job_definition)


def create_jobs(glue_client, names: list[str], conns: list[list[str]] = None) -> None:
    """genetate basic glue job with optional connectors

    Keyword arguments:
    glue_client -- boto3 glue client
    names -- list of Glue Job names
    conns -- list of a list of connector for each Glue Job
    """
    if conns:
        for name, conn in zip(names, conns):
            create_job(glue_client, name, conn)
    else:
        for name in names:
            create_job(glue_client, name)


def create_connection(glue_client, name, subnet_id=None) -> None:
    """Create Glue Job Connector associated to a given subnet

    Keyword arguments:
    glue_client -- aws boto3 glue client
    name -- name of glue connector
    subnet_id -- id of subnet to assocate with
    """

    glue_client.create_connection(
        ConnectionInput={
            "Name": name,
            "ConnectionProperties": {},
            "ConnectionType": "CUSTOM",
            "PhysicalConnectionRequirements": {
                "SubnetId": subnet_id if subnet_id else "gj_subnet",
                "SecurityGroupIdList": ["sg-0123456789abcdef0"],
                "AvailabilityZone": "eu-west-1a",
            },
        }
    )


def create_connections(
    glue_client, names: list[str], subnet_id: list[str] = None
) -> None:
    """create multiple glue connetions

    Keyword arguments:
    glue_client -- aws boto3 glue client
    names -- list of connector names to create
    subnet_id -- list of subnets to associate connectors to
    """

    for name in names:
        create_connection(glue_client, name, subnet_id)
