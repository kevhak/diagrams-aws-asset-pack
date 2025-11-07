from aws import (
    AWS_DARK,
    PublicSubnetCluster,
    RegionCluster,
    SecurityGroupCluster,
    VPCCluster,
)
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import User
from diagrams.aws.network import InternetGateway, Nacl, RouteTable
from diagrams.aws.storage import S3

with Diagram(
    f"EC2 to S3 Connection Architecture (updated{', dark' if AWS_DARK else ''})",
    show=False,
):
    user = User("External User")
    with RegionCluster("AWS Cloud (us-east-1)"):
        with VPCCluster():
            igw = InternetGateway("Internet Gateway")
            with PublicSubnetCluster():
                route_table = RouteTable("Route Table")
                nacl = Nacl("Network ACL")
                with SecurityGroupCluster():
                    ec2 = EC2("EC2 Instance")
        s3_bucket = S3("S3 Bucket")

    (
        user
        >> Edge(label="HTTPS")
        >> igw
        >> route_table
        >> nacl
        >> ec2
        >> Edge(label="API Calls")
        >> s3_bucket
    )
