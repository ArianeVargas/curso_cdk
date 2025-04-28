from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct


class CustomEc2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, is_prod: bool = False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Importar una VPC existente
        vpc = ec2.Vpc.from_lookup(self,
                                  "importedVPC",
                                  vpc_id="vpc-0b58a0ee3401325bf")

        # Leer script de arranque (descomentarlo si quieres usarlo)
        with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
            user_data = file.read()

        # Crear instancia EC2
        web_server = ec2.Instance(self,
                                  "WebServer001Id",
                                  instance_type=ec2.InstanceType("t2.micro"),
                                  instance_name="WebServer001",
                                  machine_image=ec2.MachineImage.generic_linux({
                                      "us-east-1": "ami-0e449927258d45bc4"
                                  }),
                                  vpc=vpc,
                                  vpc_subnets=ec2.SubnetSelection(
                                      subnet_type=ec2.SubnetType.PUBLIC
                                  ),
                                  user_data=ec2.UserData.custom(user_data)
                                  )

        # Salida con IP pública (opcional)
        CfnOutput(self,
                  "webServer001Ip",
                  description="WebServer Public Ip Address",
                  value=f"http://{web_server.instance_public_ip}"
                  )

        # Permitir tráfico HTTP entrante (opcional)
        web_server.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), description="Allow Web Traffic"
        )

        # ✅ Agregar permisos a la EC2 para poder usar SSM y leer de S3
        web_server.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )

        web_server.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )