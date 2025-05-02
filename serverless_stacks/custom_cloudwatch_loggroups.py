from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_logs as _logs
)
from constructs import Construct
import os


class CustomLoggroupStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Ruta al archivo fuente de la Lambda
        lambda_path = "serverless_stacks/lambda_src/konstone_processor.py"

        # Leer el código de la función Lambda
        try:
            with open(lambda_path, mode="r") as f:
                konstone_fn_code = f.read()
        except OSError:
            raise FileNotFoundError(f"No se pudo leer el código de la Lambda en: {lambda_path}")

        # Crear la función Lambda
        konstone_fn = _lambda.Function(
            self,
            "KonstoneFunction",
            function_name="konstone_function",
            runtime=_lambda.Runtime.PYTHON_3_12, 
            handler="konstone_processor.lambda_handler",  
            code=_lambda.InlineCode(konstone_fn_code),
            timeout=Duration.seconds(3),
            environment={
                "LOG_LEVEL": "INFO"
            }
        )

        # Crear grupo de logs personalizado con eliminación automática
        _logs.LogGroup(
            self,
            "KonstoneLogGroup",
            log_group_name=f"/aws/lambda/{konstone_fn.function_name}",
            removal_policy=RemovalPolicy.DESTROY
        )
