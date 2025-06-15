"""tests for AWS Boto3 Glue client wrapper"""

from test.unit.helper import create_connection, create_job, create_jobs

from awsglueavailability.client import Conn, Glue, Job, jobs_by_subnet


def test_list_gluejobs(glue_client):
    """tests successfully retrieve a list of Glue Jobs (happy path)"""

    # setup
    job_names = ["glue_job_1", "glue_job_2"]
    create_jobs(glue_client, job_names)

    # action
    glue = Glue(glue_client)

    # result
    expected_result = job_names
    actual_result = list(glue.list_jobs())

    assert expected_result == actual_result, "failed to get correct job names"


def test_list_jobs_pagination(glue_client):
    """test list pagination logic"""

    # setup
    job_names = ["glue_job_1", "glue_job_2"]
    create_jobs(glue_client, job_names)

    page_size = 1
    glue = Glue(glue_client, page_size)

    # result
    expected_result = job_names
    actual_result = list(glue.list_jobs())

    assert expected_result == actual_result, "failed to get correct job names"


def test_get_job_with_connections(glue_client):
    """test retrieval of associated Glue job connectors"""

    # setup
    create_connection(glue_client, "gj_conn")
    create_job(glue_client, "glue_job", ["gj_conn"])

    glue = Glue()

    expected_result = [
        Job(
            name="glue_job",
            conns=[Conn(name="gj_conn", subnet="gj_subnet", az="eu-west-1a")],
        )
    ]

    actual_result = glue.get_jobs()

    assert (
        expected_result == actual_result
    ), "failed to retreive glue jobs with connection details"


def test_jobs_by_subnet():
    """test remodel list of jobs to dictionary of key subnet"""

    glue_job_1 = Job(
        name="glue_job_1",
        conns=[Conn(name="glue_job_1_conn", subnet="gj_subnet1", az="eu-west-1a")],
    )

    glue_job_2 = Job(
        name="glue_job_2",
        conns=[Conn(name="glue_job_2_conn", subnet="gj_subnet2", az="eu-west-1a")],
    )

    jobs = [glue_job_1, glue_job_2]

    expected_result = {"gj_subnet1": [glue_job_1], "gj_subnet2": [glue_job_2]}

    actual_result = jobs_by_subnet(jobs)

    assert expected_result == actual_result


def test_jobs_by_subnet_multi_connectors():
    """test compatability of multiconnectors per Glue job"""

    glue_job_1 = Job(
        name="glue_job_1",
        conns=[
            Conn(name="glue_job_1_conn", subnet="gj_subnet1", az="eu-west-1a"),
            Conn(name="glue_job_2_conn", subnet="gj_subnet2", az="eu-west-1a"),
        ],
    )

    glue_job_2 = Job(
        name="glue_job_2",
        conns=[Conn(name="glue_job_3_conn", subnet="gj_subnet2", az="eu-west-1a")],
    )

    jobs = [glue_job_1, glue_job_2]

    expected_result = {
        "gj_subnet1": [glue_job_1],
        "gj_subnet2": [glue_job_1, glue_job_2],
    }

    actual_result = jobs_by_subnet(jobs)

    assert expected_result == actual_result
