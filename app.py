#!/usr/bin/env python3
import os

import aws_cdk as cdk

#from curso_cdk_practica.curso_cdk_practica_stack import CursoCdkPracticaStack
from resource_stacks.custom_vpc import CustomVpcStack
from resource_stacks.custom_ec2 import CustomEc2Stack
from resource_stacks.custom_ec2_with_lates_ami import CustomEc2LatestAmiStack
from resource_stacks.custom_ec2_with_ebs_piops import CustomEc2PiopsStack
from resource_stacks.custom_iam_users_groups import CustomIamUsersGroupsStack
from resource_stacks.custom_iam_roles_policies import CustomRolesPoliciesStack
from resource_stacks.custom_s3_resource_policy import CustomS3ResourcePolicyStack
from resource_stacks.custom_sns import CustomSnsStack
from resource_stacks.custom_sqs import CustomSqsStack

from serverless_stacks.custom_lambda import CustomLambdaStack

# VPC, EC2, ALB, RDS Stack
from app_db_stack.vpc_3tier_stack import Vpc3TierStack
from app_db_stack.web_server_3tier_stack import WebServer3TierStack
from app_db_stack.rds_3tier_stack import RdsDatabase3TierStack

from stacks_from_cfn.stack_from_existing_cfn_template import StackFromCloudFormationTemplate

from app_stacks.vpc_stack import VpcStack
from app_stacks.web_server_stack import WebServerStack


app = cdk.App()

# CustomVpcStack(app, "CustomVpcStack",
#                is_prod=True,
#                env=cdk.Environment(account="987227712684", region="us-east-1"))

# CustomEc2Stack(app, "CustomEc2Stack",
#                is_prod=True,
#                env=cdk.Environment(account="987227712684", region="us-east-1"))

# CustomEc2LatestAmiStack(app, "CustomEc2LatestAmiStack",
#                         is_prod=True,
#                         env=cdk.Environment(account="987227712684", region="us-east-2"))

# CustomEc2PiopsStack(app, "CustomEc2PiopsStack",
#                         is_prod=True,
#                         env=cdk.Environment(account="987227712684", region="us-east-1"))

# vpc_stack = VpcStack(app, "multi-tier-app-vpc-stack")
# ec2_stack = WebServerStack(
#     app, "multi-tier-app-web-server-stack", vpc=vpc_stack.vpc)

# iam_users_groups_stack = CustomIamUsersGroupsStack(
#     app,
#     "custom-iam-users-groups-stack",
#     description="Create IAM User & Groups"
# )

# custom_iam_roles_policies = CustomRolesPoliciesStack(
#     app,
#     "custom-iam-roles-policies-stack",
#     description="Create IAM Roles & Policies"
# )

# custom_s3_resource_policy = CustomS3ResourcePolicyStack(
#     app,
#     "custom-s3-esource-policy-stack",
#     description="Create S3 Resource Policy"
# )

# Create 3Tier App with App Servers in ASG and Backend as RDS Database
# vpc_3tier_stack = Vpc3TierStack(app, "multi-tier-app-vpc-stack")
# app_3tier_stack = WebServer3TierStack(
#     app, "multi-tier-app-web-server-stack", vpc=vpc_3tier_stack.vpc)
# db_3tier_stack = RdsDatabase3TierStack(
#     app,
#     "multi-tier-app-db-stack",
#     vpc=vpc_3tier_stack.vpc,
#     asg_security_groups=app_3tier_stack.web_server_asg.connections.security_groups,
#     description="Create Custom RDS Database"
# )

# Resource Stack from pre-existing Cloudformation Template
# stack_from_cfn = StackFromCloudFormationTemplate(app,
#                                                  "stack-from-pre-existing-cfn",
#                                                  description="Resource Stack from pre-existing Cloudformation Template"
#                                                  )

# Create SNS Topics & Add Email Subscriptions
# custom_sns = CustomSnsStack(
#     app,
#     "custom-sns-stack",
#     description="Create SNS Topics & Add Email Subscriptions"
# )

# Create SQS for microservices
# custom_sqs = CustomSqsStack(
#     app,
#     "custom-sqs-stack",
#     description="Create a fully managed message queues for microservices"
# )

# Create Serverless Event Processor using Lambda
custom_lambda = CustomLambdaStack(
    app,
   "custom-lambda-stack",
    description="Create Serverless Event Processor using Lambda"
)


app.synth()
