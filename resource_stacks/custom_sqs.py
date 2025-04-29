from aws_cdk import (
    Stack,
    Duration,
    aws_sqs as sqs
)
from constructs import Construct


class CustomSqsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear la cola SQS FIFO con cifrado y configuración personalizada
        konstone_queue = sqs.Queue(
            self,
            "KonstoneQueue",
            queue_name="konstone_queue.fifo",
            fifo=True,
            encryption=sqs.QueueEncryption.KMS_MANAGED,
            retention_period=Duration.days(4),
            visibility_timeout=Duration.seconds(45)
        )
