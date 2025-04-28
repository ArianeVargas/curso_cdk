from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_s3 as s3,
    Tags,
)
from constructs import Construct


class CustomVpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, is_prod: bool = False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Obtener configuración del contexto
        prod_configs = self.node.try_get_context('envs')['prod']

        # Crear VPC personalizada
        custom_vpc = ec2.Vpc(
            self,
            "CustomVpcId",
            ip_addresses=ec2.IpAddresses.cidr(prod_configs['vpc_configs']['vpc_cidr']),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="publicSubnet",
                    cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                ec2.SubnetConfiguration(
                    name="privateSubnet",
                    cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                ec2.SubnetConfiguration(
                    name="dbSubnet",
                    cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                ),
            ]
        )

        # Salida de la VPC
        CfnOutput(self,
                  "CustomVpcOutput",
                  value=custom_vpc.vpc_id,
                  export_name="CustomVpcId")
        
        
        # Crear un bucket nuevo
        my_bkt = s3.Bucket(self, "CustomBucketId")
        Tags.of(my_bkt).add("Owner", "Mystique")
        
        # Importar un bucket por nombre
        bkt1 = s3.Bucket.from_bucket_name(
            self,
            "MyImportedBucket",
            "sample-bkt-cdk-012"
        )
        
         # Importar un bucket por ARN
        bkt2 = s3.Bucket.from_bucket_arn(
            self,
            "CrossAccountBucket",
            "arn:aws:s3:::SAMPLE-CROSS-BUCKET"
        )
        
        CfnOutput(self,
                  "MyImportedBucketName",
                  value=bkt1.bucket_name)
        
        # Importar una VPC existente por ID
        vpc2 = ec2.Vpc.from_lookup(self,
                                   "ImportedVPC",
                                   vpc_id="vpc-0b58a0ee3401325bf"
                                   )

        CfnOutput(self,
                  "ImportedVpc2Id",
                  value=vpc2.vpc_id)
        
        # Crear conexión de peering entre VPCs
        ec2.CfnVPCPeeringConnection(self,
                                    "PeerVpc12",
                                    vpc_id=custom_vpc.vpc_id,
                                    peer_vpc_id=vpc2.vpc_id)
        
        