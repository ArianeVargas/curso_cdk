from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    RemovalPolicy,
)
from constructs import Construct
import os


class CustomPrivilegesToLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        konstone_s3_assets_table = dynamodb.Table(
            self,
            "KonstoneAssetsDDBTable",
            table_name="konstone-asset-pkon-table",
            partition_key=dynamodb.Attribute(
                name="_id",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY  # solo para dev/testing
        )

        # Read Lambda Code
        lambda_file_path = "serverless_stacks/lambda_src/konstone_s3_inventory_generator.py"
        try:
            with open(lambda_file_path, "r") as f:
                konstone_fn_code = f.read()
        except OSError as e:
            raise RuntimeError(f"Unable to read Lambda code from {lambda_file_path}") from e

        # Lambda Function
        konstone_fn = _lambda.Function(
            self,
            "KonstoneFunction",
            function_name="konstone_function_s3_inventory_generator",
            runtime=_lambda.Runtime.PYTHON_3_11,  # Actualizado de 3.7 a 3.11
            handler="index.lambda_handler",
            code=_lambda.InlineCode(konstone_fn_code),
            timeout=Duration.seconds(3),
            environment={
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": konstone_s3_assets_table.table_name
            }
        )

        # IAM: S3 ReadOnlyAccess policy
        konstone_fn.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )

        # Grant DynamoDB write access
        konstone_s3_assets_table.grant_write_data(konstone_fn)
