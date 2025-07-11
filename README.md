# aws-glue-availability

[AWS Glue](https://aws.amazon.com/glue) provides disaster / recovery through Glue ETL retry mechanism testing for the successful connector starting with the first referenced working to the last incrementally until it finds a successful connection. To ensure a certain level of high availability (all be it not in the strictest of senses) multiple connectors need to be associated across different [Availability Zones](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/).

This tool is to aid in viewing the placement of Glue Jobs through their associated Connectors Subnet information, to provide a visual aid in understanding the distribution of Glue jobs across the VPCs / Subnets within your platform.

## Running

This tool is currently containing a Python interface.

```shell
#install library from PyPi
pip install awsglueavailability

#run application
#ensure AWS Credentials are setup
python -m awsglueavailability
```

## Permissions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AwsIamMapper",
      "Action": [
        "glue:ListJobs",
        "glue:GetConnection",
        "vpc:DescribeSubnets"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

## Example Output
An output is generated 
![example](img/example.png)


## References
- [Glue Failover behaviour](https://docs.aws.amazon.com/glue/latest/dg/glue-troubleshooting-errors.html#vpc-failover-behavior-error-10)
- [Diagrams library](https://diagrams.mingrammer.com/)