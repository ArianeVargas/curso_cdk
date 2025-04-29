import json
from aws_cdk import (
    Stack,
    CfnOutput,
    Fn,
)
from aws_cdk.cloudformation_include import CfnInclude
from constructs import Construct


class StackFromCloudFormationTemplate(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Cargar plantilla CloudFormation existente (JSON)
        try:
            with open("stacks_from_cfn/sample_templates/create_s3_bucket_template.json", mode="r") as file:
                cfn_template = json.load(file)
        except OSError:
            raise RuntimeError("No se pudo leer la plantilla de CloudFormation")

        # Incluir la plantilla en el stack de CDK
        resources_from_cfn_template = CfnInclude(
            self,
            "KonstoneInfra",
            template_file="stacks_from_cfn/sample_templates/create_s3_bucket_template.json"
        )

        # Obtener el ARN del bucket encriptado
        encrypted_bucket_arn = Fn.get_att("EncryptedS3Bucket", "Arn").to_string()

        # Salida del ARN
        CfnOutput(
            self,
            "EncryptedBucketArn",
            value=encrypted_bucket_arn,
            description="ARN del bucket encriptado importado desde la plantilla CloudFormation"
        )
