from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_kms as kms,
    RemovalPolicy,
)
from constructs import Construct


class CursoCdkPracticaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, is_prod: bool = False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Recuperar ARN de la clave KMS desde el contexto (si está en prod)
        context_prod = self.node.try_get_context('prod') or {}
        kms_arn = context_prod.get('kms_arn') if is_prod else None

        if is_prod:
            if kms_arn:
                # Si se proporcionó un ARN de clave, la importamos
                mykey = kms.Key.from_key_arn(self, "MyImportedKey", kms_arn)
            else:
                # Si no hay ARN, se crea una nueva clave
                mykey = kms.Key(self, "MyGeneratedKmsKey")

            # Crear bucket en entorno de producción con cifrado KMS
            artifact_bucket = s3.Bucket(self,
                                        "MyProdArtifactBucket",
                                        versioned=True,
                                        encryption=s3.BucketEncryption.KMS,
                                        encryption_key=mykey,
                                        removal_policy=RemovalPolicy.RETAIN)
        else:
            # Crear bucket en entorno de desarrollo (sin cifrado KMS)
            artifact_bucket = s3.Bucket(self,
                                        "MyDevArtifactBucket",
                                        removal_policy=RemovalPolicy.DESTROY)
            
    
