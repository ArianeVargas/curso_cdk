from aws_cdk import (
    Stack,
    Aws,
    CfnOutput,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class CustomRolesPoliciesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Secret for User1 Password
        user1_pass = secretsmanager.Secret(
            self,
            "user1Pass",
            description="Password for User1",
            secret_name="user1_pass"
        )

        # IAM User with password from Secrets Manager
        user1 = iam.User(
            self,
            "user1",
            password=user1_pass.secret_value,
            user_name="user1"
        )

        # IAM Group
        konstone_group = iam.Group(
            self,
            "konStoneGroup",
            group_name="konstone_group"
        )

        # Add User to Group
        konstone_group.add_user(user1)

        # Attach Managed Policy to Group
        konstone_group.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )
        )

        # SSM Parameter 1
        param1 = ssm.StringParameter(
            self,
            "parameter1",
            description="Keys To KonStone",
            parameter_name="/konstone/keys/fish",
            string_value="130481",
            tier=ssm.ParameterTier.STANDARD
        )

        # SSM Parameter 2
        param2 = ssm.StringParameter(
            self,
            "parameter2",
            description="Keys To KonStone",
            parameter_name="/konstone/keys/fish/gold",
            string_value="130482",
            tier=ssm.ParameterTier.STANDARD
        )

        # Grant Group permission to read Parameter 1
        param1.grant_read(konstone_group)

        # Policy Statement to describe parameters
        describe_parameters_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ssm:DescribeParameters"],
            resources=["*"]
        )
        describe_parameters_statement.sid = "DescribeAllParametersInConsole"

        konstone_group.add_to_policy(describe_parameters_statement)

        # Create IAM Role
        konstone_ops_role = iam.Role(
            self,
            "konstoneOpsRole",
            assumed_by=iam.AccountPrincipal(Aws.ACCOUNT_ID),
            role_name="konstone_ops_role"
        )

        # Create Managed Policy & Attach to Role
        list_ec2_policy = iam.ManagedPolicy(
            self,
            "listEc2Instances",
            description="List EC2 instances and CloudWatch data",
            managed_policy_name="list_ec2_policy",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "cloudwatch:Get*"
                    ],
                    resources=["*"]
                )
            ],
            roles=[konstone_ops_role]
        )

        # Login URL Output
        CfnOutput(
            self,
            "user1LoginUrl",
            description="Login URL for User1",
            value=f"https://{Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
        )
