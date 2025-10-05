from aws import (
    AWS_DARK,
    EDGE_ATTR,
    GRAPH_ATTR,
    NODE_ATTR,
    PUBLIC_SUBNET,
    REGION,
    SECURITY_GROUP,
    VPC,
)
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import User
from diagrams.aws.network import InternetGateway, Nacl, RouteTable
from diagrams.aws.storage import S3

with Diagram(
    f"EC2 to S3 Connection Architecture (updated{', dark' if AWS_DARK else ''})",
    show=False,
    graph_attr=GRAPH_ATTR,
    node_attr=NODE_ATTR,
    edge_attr=EDGE_ATTR,
):
    user = User("External User")
    with Cluster("AWS Cloud (us-east-1)", graph_attr=REGION):
        with Cluster("VPC", graph_attr=VPC):
            igw = InternetGateway("Internet Gateway")
            with Cluster("Public Subnet", graph_attr=PUBLIC_SUBNET):
                route_table = RouteTable("Route Table")
                nacl = Nacl("Network ACL")
                with Cluster("Security Group", graph_attr=SECURITY_GROUP):
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
