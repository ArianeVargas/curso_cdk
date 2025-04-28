from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct


class CustomS3ResourcePolicyStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear el bucket de S3 con Bloqueo de Acceso Público desactivado
        konstone_bkt = s3.Bucket(
            self,
            "konstoneAssets",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                ignore_public_acls=False,
                block_public_policy=False,
                restrict_public_buckets=False
            )
        )

        # Agregar política de recurso: permitir acceso público a archivos .html
        konstone_bkt.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[konstone_bkt.arn_for_objects("*.html")],
                principals=[iam.AnyPrincipal()]
            )
        )

        # Agregar política de recurso: denegar accesos que no sean HTTPS
        konstone_bkt.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{konstone_bkt.bucket_arn}/*"],
                principals=[iam.AnyPrincipal()],
                conditions={
                    "Bool": {"aws:SecureTransport": "false"}
                }
            )
        )