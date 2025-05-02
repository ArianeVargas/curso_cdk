from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
)
from constructs import Construct

class CustomLambdaAsCronStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Leer el código fuente de Lambda
        try:
            with open("serverless_stacks/lambda_src/konstone_processor.py", mode="r") as f:
                konstone_fn_code = f.read()
        except OSError:
            print("No se pudo leer el código de la función Lambda")
            konstone_fn_code = ""

        # Crear la función Lambda
        konstone_fn = _lambda.Function(
            self,
            "konstoneFunction",
            function_name="konstone_function",
            runtime=_lambda.Runtime.PYTHON_3_10,  # actualizado a versión más reciente
            handler="index.lambda_handler",
            code=_lambda.InlineCode(konstone_fn_code),
            timeout=Duration.seconds(3),
            environment={
                "LOG_LEVEL": "INFO",
                "AUTOMATION": "SKON"
            }
        )

        # Regla de CloudWatch para las 18:00 UTC de lunes a viernes
        six_pm_cron = _events.Rule(
            self,
            "sixPmRule",
            schedule=_events.Schedule.cron(
                minute="0",
                hour="18",
                month="*",
                week_day="MON-FRI",
                year="*"
            )
        )

        # Regla basada en frecuencia: cada 3 minutos
        run_every_3_minutes = _events.Rule(
            self,
            "runEvery3Minutes",
            schedule=_events.Schedule.rate(Duration.minutes(3))
        )

        # Asociar la función Lambda como objetivo de las reglas
        six_pm_cron.add_target(_targets.LambdaFunction(konstone_fn))
        run_every_3_minutes.add_target(_targets.LambdaFunction(konstone_fn))
