from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
)
from constructs import Construct

class VpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "customVpcId",
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="app", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                ec2.SubnetConfiguration(
                    name="db", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                )
            ]
        )

        CfnOutput(
            self,
            "customVpcOutput",
            value=self.vpc.vpc_id,
            export_name="VpcId"
        )
