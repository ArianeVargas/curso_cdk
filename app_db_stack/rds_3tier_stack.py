from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    Duration,
    aws_rds as rds,
    aws_ec2 as ec2,
)
from constructs import Construct


class RdsDatabase3TierStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, asg_security_groups: list, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear una instancia RDS MySQL
        konstone_db = rds.DatabaseInstance(
            self,
            "konstoneRDS",
            vpc=vpc,
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_34
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO
            ),
            allocated_storage=30,
            multi_az=False,
            cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
            database_name="konstone_db",
            credentials=rds.Credentials.from_username("mystiquemaster"),
            port=3306,
            deletion_protection=False,
            delete_automated_backups=True,
            backup_retention=Duration.days(7),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Permitir a los security groups del ASG acceder al puerto por defecto (3306) del RDS
        for sg in asg_security_groups:
            konstone_db.connections.allow_default_port_from(
                sg,
                "Permitir acceso del ASG EC2 al RDS MySQL"
            )

        # Output con el comando para conectarse a la base de datos
        CfnOutput(
            self,
            "DatabaseConnectionCommand",
            value=f"mysql -h {konstone_db.db_instance_endpoint_address} -P 3306 -u mystiquemaster -p",
            description="Conéctate a la base de datos usando este comando"
        )
