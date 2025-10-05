from aws import AWS_DARK, EDGE_ATTR, GENERIC_GROUP, GRAPH_ATTR, NODE_ATTR
from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3

with Diagram(
    f"Event Processing (updated{', dark' if AWS_DARK else ''})",
    show=False,
    graph_attr=GRAPH_ATTR,
    node_attr=NODE_ATTR,
    edge_attr=EDGE_ATTR,
):
    source = EKS("k8s source")

    with Cluster("Event Flows", graph_attr=GENERIC_GROUP):
        with Cluster("Event Workers", graph_attr=GENERIC_GROUP):
            workers = [ECS("worker1"), ECS("worker2"), ECS("worker3")]

        queue = SQS("event queue")

        with Cluster("Processing", graph_attr=GENERIC_GROUP):
            handlers = [Lambda("proc1"), Lambda("proc2"), Lambda("proc3")]

    store = S3("events store")
    dw = Redshift("analytics")

    source >> workers >> queue >> handlers
    handlers >> store
    handlers >> dw
