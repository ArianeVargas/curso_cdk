from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    CfnOutput,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_logs as logs,
)
from constructs import Construct

class CustomApiGatewayStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Intenta leer el código fuente desde un archivo
        try:
            with open("serverless_stacks/lambda_src/konstone_hello_world.py", mode="r") as f:
                konstone_fn_code = f.read()
        except OSError:
            print("⚠️ No se pudo leer el código fuente de la Lambda. Usando código por defecto.")
            konstone_fn_code = """
def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hola desde Lambda (fallback)'
    }
"""

        # Crear la función Lambda
        konstone_fn = lambda_.Function(
            self,
            "konstoneFunction",
            function_name="konstone_function",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="index.handler",  # <--- aquí debe ser index.handler porque usamos InlineCode
            code=lambda_.InlineCode(konstone_fn_code),
            timeout=Duration.seconds(3),
            environment={
                "LOG_LEVEL": "INFO",
                "Environment": "Production"
            }
        )

        # Crear grupo de logs para la Lambda
        logs.LogGroup(
            self,
            "konstoneLoggroup",
            log_group_name=f"/aws/lambda/{konstone_fn.function_name}",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Crear API Gateway conectado a la Lambda
        konstone_api = apigateway.LambdaRestApi(
            self,
            "konstoneApiEndpoint",
            handler=konstone_fn
        )

        # Exportar la URL de la API como salida del stack
        CfnOutput(
            self,
            "ApiUrl",
            value=konstone_api.url,
            description="Use un navegador para acceder a esta URL"
        )
