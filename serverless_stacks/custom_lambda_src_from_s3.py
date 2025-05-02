from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3,
)
from constructs import Construct


class CustomLambdaSrcFromS3Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Importar el bucket S3 existente
        konstone_bkt = _s3.Bucket.from_bucket_attributes(
            self,
            "konstoneAssetsBucket",
            bucket_name="konstone-assets-bkt"
        )

        # Crear la función Lambda usando código desde S3
        konstone_fn = _lambda.Function(
            self,
            "konstoneFunction",
            function_name="konstone_fn",
            runtime=_lambda.Runtime.PYTHON_3_12,  
            handler="konstone_processor.lambda_handler",
            code=_lambda.Code.from_bucket(
                bucket=konstone_bkt,
                key="lambda_src/konstone_processor.zip"
            ),
            timeout=Duration.seconds(2)
        )

        # Crear un grupo de logs personalizado con retención de 1 semana
        konstone_lg = _logs.LogGroup(
            self,
            "konstoneLoggroup",
            log_group_name=f"/aws/lambda/{konstone_fn.function_name}",
            removal_policy=RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_WEEK
        )
