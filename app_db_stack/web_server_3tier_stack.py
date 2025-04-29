from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_autoscaling as autoscaling,
)
from constructs import Construct


class WebServer3TierStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Leer el script de arranque (user data)
        try:
            with open("app_db_stack/user_data/deploy_app.sh", mode="r") as file:
                user_data = file.read()
        except OSError:
            print('No se pudo leer el script de UserData')

        # Imagen de Amazon Linux 2
        linux_ami = ec2.AmazonLinuxImage(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Crear el Application Load Balancer (ALB)
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "myAlbId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )

        # Permitir tráfico HTTP (puerto 80) desde Internet al ALB
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80),
            description="Allow Internet access on ALB Port 80"
        )

        # Añadir listener en el puerto 80
        listener = alb.add_listener("listenerId",
                                    port=80,
                                    open=True)

        # Crear IAM Role para los servidores web
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
        self.web_server_asg = autoscaling.AutoScalingGroup(
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

        # Permitir que el ALB envíe tráfico a las instancias del ASG
        self.web_server_asg.connections.allow_from(
            alb,
            ec2.Port.tcp(80),
            description="Allows ASG Security Group receive traffic from ALB"
        )

        # Añadir las instancias del ASG al target group del ALB
        listener.add_targets("asgTargetGroup",
                             port=80,
                             targets=[self.web_server_asg])

        # Output del nombre DNS del Load Balancer
        CfnOutput(
            self,
            "albDomainName",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Web Server ALB Domain Name"
        )
