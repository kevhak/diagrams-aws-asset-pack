from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import User
from diagrams.aws.network import InternetGateway, Nacl, RouteTable
from diagrams.aws.storage import S3

with Diagram(
    "EC2 to S3 Connection Architecture",
    show=False,
):
    user = User("External User")
    with Cluster("AWS Cloud (us-east-1)"):
        with Cluster("VPC"):
            igw = InternetGateway("Internet Gateway")
            with Cluster("Public Subnet"):
                route_table = RouteTable("Route Table")
                nacl = Nacl("Network ACL")
                with Cluster("Security Group"):
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
