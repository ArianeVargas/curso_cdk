from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct


class CustomEc2PiopsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, is_prod: bool = False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Crear una VPC con una subred pública sin NAT
        vpc = ec2.Vpc(
            self,
            "customVpcId",
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/24"),
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC
                )
            ]
        )

        # Leer script de arranque desde archivo
        try:
            with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print("Unable to read UserData script")
            user_data = ""

        # Obtener la última AMI de Amazon Linux 2
        amzn_linux_ami = ec2.MachineImage.latest_amazon_linux2()

        # Crear la instancia EC2
        web_server = ec2.Instance(
            self,
            "WebServer004Id",
            instance_type=ec2.InstanceType("t2.micro"),
            instance_name="WebServer004",
            machine_image=amzn_linux_ami,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            user_data=ec2.UserData.custom(user_data)
        )

        # Añadir EBS con almacenamiento provisionado de IOPS (IO1)
        web_server.instance.add_property_override(
            "BlockDeviceMappings", [
                {
                    "DeviceName": "/dev/sdb",
                    "Ebs": {
                        "VolumeSize": "8",
                        "VolumeType": "io1",
                        "Iops": "400",
                        "DeleteOnTermination": True
                    }
                }
            ]
        )

        # Mostrar la IP pública como salida del stack
        CfnOutput(
            self,
            "WebServer004Ip",
            description="WebServer Public Ip Address",
            value=f"http://{web_server.instance_public_ip}"
        )

        # Permitir tráfico HTTP (puerto 80)
        web_server.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), description="Allow Web Traffic"
        )

        # Agregar permisos necesarios para SSM y acceso a S3
        web_server.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )

        web_server.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )
