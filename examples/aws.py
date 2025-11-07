"""AWS Diagrams Enhancement Module

This module enhances the diagrams library to create more professional-looking AWS architecture diagrams
that align with AWS visual design guidelines. When imported, it automatically applies AWS-specific styling,
colors, and provides specialized cluster classes for common AWS components.

Features:
- Automatic dark mode support via AWS_DARK environment variable
- AWS official color palette and styling attributes
- Pre-configured cluster classes for AWS components (VPC, Subnets, Security Groups, etc.)
- Monkey-patched Diagram and Cluster classes with AWS defaults
- Enhanced visual consistency with AWS architecture icons

Usage:
    import aws  # Automatically enhances all diagrams with AWS styling

    # Dark mode can be enabled by setting environment variable:
    # AWS_DARK=1 python your_diagram.py
"""

import os

AWS_DARK = os.getenv("AWS_DARK", "").lower() in ("1", "true")

if AWS_DARK:
    from diagrams.aws import general

    for general_name in dir(general):
        cls = getattr(general, general_name)
        if hasattr(cls, "_icon") and cls._icon and cls._icon.endswith(".png"):  # pylint: disable=protected-access
            dark_icon = cls._icon.replace(".png", "-dark.png")  # pylint: disable=protected-access
            # Modify the original module
            setattr(
                general, general_name, type(general_name, (cls,), {"_icon": dark_icon})
            )

if AWS_DARK:
    AWS_BG_COLOR = "#000000"
    AWS_FG_COLOR = "#FFFFFF"
    AWS_ARROW_COLOR = "#9BA7B6"
else:
    AWS_BG_COLOR = "#FFFFFF"
    AWS_FG_COLOR = "#000000"
    AWS_ARROW_COLOR = "#000000"

# fmt: off
# AWS color palette
AWS_COLOR_SQUID = "#232F3E"
AWS_COLOR_GRAY = "#7D8998"  # (borders)
AWS_COLOR_NEBULA = "#C925D1"  # (blue replacement) Customer Enablement; Database; Developer Tools; Satellite
AWS_COLOR_ENDOR = "#7AA116"  # (green) Cloud Financial Management; Internet of Things; Storage
AWS_COLOR_SMILE = "#ED7100"  # (orange) Blockchain; Compute; Containers; Media Services; Quantum Technologies
AWS_COLOR_COSMOS = "#E7157B"  # (pink) Application Integration; Management & Governance
AWS_COLOR_GALAXY = "#8C4FFF"  # (purple) Analytics; Games; Networking & Content Delivery; Serverless
AWS_COLOR_MARS = "#DD344C"  # (red) Business Applications; Contact Center; Front-End Web & Mobile; Robotics; Security, Identity & Compliance
AWS_COLOR_ORBIT = "#01A88D"  # (turquoise) Artificial Intelligence; End User Computing; Migration & Modernization
# fmt: on

# https://www.graphviz.org/doc/info/attrs.html

AWS_GRAPH_ATTR = {
    "fontsize": "24",
    "fontcolor": AWS_FG_COLOR,
    "bgcolor": AWS_BG_COLOR,
    "ranksep": "1.0",
}

AWS_CLUSTER_ATTR = {
    "bgcolor": AWS_BG_COLOR,
    "fillcolor": AWS_BG_COLOR,
    "labeljust": "l",
    "margin": "24",
    "fontcolor": AWS_FG_COLOR,
    "fontname": "Arial",
    "fontsize": "18",
    "style": "diagonals",
    "penwidth": "3",
}

AWS_NODE_ATTR = {
    "fillcolor": AWS_BG_COLOR,
    "fontcolor": AWS_FG_COLOR,
    "fontname": "Arial",
}

AWS_EDGE_ATTR = {
    "fillcolor": AWS_ARROW_COLOR,
    "color": AWS_ARROW_COLOR,
    "fontcolor": AWS_FG_COLOR,
    "labelfontcolor": AWS_FG_COLOR,
    "arrowhead": "vee",
    "arrowsize": "1.25",
    "style": "bold",
}

AWS_REGION_ATTR = AWS_CLUSTER_ATTR | {"pencolor": AWS_COLOR_ORBIT, "style": "dotted"}
AWS_AVAILABILITY_ZONE_ATTR = AWS_CLUSTER_ATTR | {
    "pencolor": AWS_COLOR_ORBIT,
    "style": "dashed",
}
AWS_SECURITY_GROUP_ATTR = AWS_CLUSTER_ATTR | {
    "pencolor": AWS_COLOR_MARS,
    "labeljust": "c",
}
AWS_VPC_ATTR = AWS_CLUSTER_ATTR | {"pencolor": AWS_COLOR_GALAXY}
AWS_PUBLIC_SUBNET_ATTR = AWS_CLUSTER_ATTR | {"pencolor": AWS_COLOR_ENDOR}
AWS_PRIVATE_SUBNET_ATTR = AWS_CLUSTER_ATTR | {"pencolor": AWS_COLOR_ORBIT}
AWS_GENERIC_GROUP_ATTR = AWS_CLUSTER_ATTR | {
    "pencolor": AWS_COLOR_GRAY,
    "labeljust": "c",
    "style": "dashed",
}


# Monkey-patch Diagram to use AWS defaults
from diagrams import Diagram  # pylint: disable=wrong-import-position  # noqa: E402

_original_diagram_init = Diagram.__init__


def _aws_diagram_init(
    self, name="", graph_attr=None, node_attr=None, edge_attr=None, **kwargs
):
    if graph_attr is None:
        graph_attr = AWS_GRAPH_ATTR
    if node_attr is None:
        node_attr = AWS_NODE_ATTR
    if edge_attr is None:
        edge_attr = AWS_EDGE_ATTR
    _original_diagram_init(
        self,
        name,
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        **kwargs,
    )


Diagram.__init__ = _aws_diagram_init

# Monkey-patch Cluster to use AWS defaults
from diagrams import Cluster  # pylint: disable=wrong-import-position  # noqa: E402

_original_cluster_init = Cluster.__init__


def _aws_cluster_init(self, label="", graph_attr=None, **kwargs):
    if graph_attr is None:
        graph_attr = AWS_GENERIC_GROUP_ATTR
    _original_cluster_init(self, label, graph_attr=graph_attr, **kwargs)


Cluster.__init__ = _aws_cluster_init


class RegionCluster(Cluster):
    """A cluster with defaults for an AWS Region"""

    def __init__(self, label="Region", graph_attr=None, **kwargs):
        if graph_attr is None:
            graph_attr = AWS_REGION_ATTR
        super().__init__(label, graph_attr=graph_attr, **kwargs)


class VPCCluster(Cluster):
    """A cluster with defaults for an AWS VPC"""

    def __init__(self, label="VPC", graph_attr=None, **kwargs):
        if graph_attr is None:
            graph_attr = AWS_VPC_ATTR
        super().__init__(label, graph_attr=graph_attr, **kwargs)


class AvailabilityZoneCluster(Cluster):
    """A cluster with defaults for an AWS Availability Zone"""

    def __init__(self, label="Availability Zone", graph_attr=None, **kwargs):
        if graph_attr is None:
            graph_attr = AWS_AVAILABILITY_ZONE_ATTR
        super().__init__(label, graph_attr=graph_attr, **kwargs)


class PublicSubnetCluster(Cluster):
    """A cluster with defaults for an AWS Public Subnet"""

    def __init__(self, label="Public Subnet", graph_attr=None, **kwargs):
        if graph_attr is None:
            graph_attr = AWS_PUBLIC_SUBNET_ATTR
        super().__init__(label, graph_attr=graph_attr, **kwargs)


class PrivateSubnetCluster(Cluster):
    """A cluster with defaults for an AWS Private Subnet"""

    def __init__(self, label="Private Subnet", graph_attr=None, **kwargs):
        if graph_attr is None:
            graph_attr = AWS_PRIVATE_SUBNET_ATTR
        super().__init__(label, graph_attr=graph_attr, **kwargs)


class SecurityGroupCluster(Cluster):
    """A cluster with defaults for an AWS Security Group"""

    def __init__(self, label="Security Group", graph_attr=None, **kwargs):
        if graph_attr is None:
            graph_attr = AWS_SECURITY_GROUP_ATTR
        super().__init__(label, graph_attr=graph_attr, **kwargs)
