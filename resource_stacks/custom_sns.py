from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_sns_subscriptions as subs
)
from constructs import Construct


class CustomSnsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear el tema de SNS
        konstone_topic = sns.Topic(
            self,
            "KonstoneHotTopic",
            display_name="Últimos temas en KonStone",
            topic_name="konstoneHotTopic"
        )

        # Agregar una suscripción de correo electrónico
        konstone_topic.add_subscription(
            subs.EmailSubscription("ariane2fernanda4@gmail.com")
        )
