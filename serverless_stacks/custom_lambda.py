from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda
)
from constructs import Construct
import os


class CustomLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_path = "serverless_stacks/lambda_src/konstone_processor.py"

        try:
            with open(lambda_path, mode="r") as f:
                konstone_fn_code = f.read()
        except OSError:
            raise FileNotFoundError(f"No se pudo leer el código de la función Lambda en: {lambda_path}")

        _lambda.Function(
            self,
            "KonstoneFunction",
            function_name="konstone_function",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="konstone_processor.lambda_handler",  # debe coincidir con el archivo
            code=_lambda.InlineCode(konstone_fn_code),
            timeout=Duration.seconds(3),
            environment={
                "LOG_LEVEL": "INFO"
            }
        )
