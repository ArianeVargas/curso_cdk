from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_autoscaling as autoscaling
)
from constructs import Construct


class WebServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Leer script de arranque
        try:
            with open("bootstrap_scripts/install_httpd.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print("No se pudo leer el script de arranque")
            user_data = ""

        # AMI Amazon Linux 2
        linux_ami = ec2.MachineImage.latest_amazon_linux2()

        # Crear Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "myAlbId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )

        # Permitir tráfico desde internet al ALB
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), description="Allow HTTP from internet"
        )

        # Crear listener en puerto 80
        listener = alb.add_listener("listenerId", port=80, open=True)

        # Crear rol para instancias EC2 del Auto Scaling Group
        web_server_role = iam.Role(
            self,
            "webServerRoleId",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        # Crear Auto Scaling Group con 2 instancias EC2
        web_server_asg = autoscaling.AutoScalingGroup(
            self,
            "webServerAsgId",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=linux_ami,
            role=web_server_role,
            min_capacity=2,
            max_capacity=2,
            user_data=ec2.UserData.custom(user_data)
        )

        # Permitir tráfico del ALB a las instancias del ASG
        web_server_asg.connections.allow_from(
            alb, ec2.Port.tcp(80), description="Allow HTTP from ALB"
        )

        # Asociar ASG con el listener del ALB
        listener.add_targets("webTargetGroupId", port=80, targets=[web_server_asg])

        # Salida del nombre DNS del ALB
        CfnOutput(
            self,
            "albDomainName",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Nombre de dominio del ALB"
        )
