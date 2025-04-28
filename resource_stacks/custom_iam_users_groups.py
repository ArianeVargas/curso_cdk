from aws_cdk import (
    Stack,
    CfnOutput,
    Aws,
    SecretValue
)
from aws_cdk import aws_iam as iam
from aws_cdk import aws_secretsmanager as secretsmanager
from constructs import Construct  # <- Construct se importa separado en v2

class CustomIamUsersGroupsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear secreto en Secrets Manager para User1
        user1_pass = secretsmanager.Secret(self,
                                           "user1Pass",
                                           description="Password for User1",
                                           secret_name="user1_pass"
                                           )

        # Crear User1 usando el secreto
        user1 = iam.User(self, "user1",
                         password=user1_pass.secret_value,
                         user_name="user1"
                         )

        # Crear User2 usando una contraseña literal (NO recomendado)
        user2 = iam.User(self, "user2",
                         password=SecretValue.plain_text("Dont-Use-B@d-Passw0rds"),
                         user_name="user2"
                         )

        # Crear un grupo IAM
        konstone_group = iam.Group(self,
                                   "konStoneGroup",
                                   group_name="konstone_group"
                                   )

        # Agregar User2 al grupo
        konstone_group.add_user(user2)

        # Generar salida de la URL de inicio de sesión
        CfnOutput(self,
                  "user2LoginUrl",
                  description="Login URL for User2",
                  value=f"https://{Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
                  )
