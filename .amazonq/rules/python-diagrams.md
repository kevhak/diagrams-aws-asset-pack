# Python Diagram as Code

When generating diagrams using mingrammer Diagrams as code for the AWS Diagram MCP Server, follow the rules below when calling the `generate_diagram` tool:

- Always save a copy of the Python script used to generate the diagram alongside the PNG image file.  This is needed so the developer can make changes.
- For style reasons, use the Python code below to declare constants at the global level and before the `with Diagram` block.
    ```python
    AWS_DARK = False
    
    if AWS_DARK:
        AWS_BG_COLOR = "#000000"
        AWS_FG_COLOR = "#FFFFFF"
        AWS_ARROW_COLOR = "#9BA7B6"
    else:
        AWS_BG_COLOR = "#FFFFFF"
        AWS_FG_COLOR = "#000000"
        AWS_ARROW_COLOR = "#000000"
    
    AWS_COLOR_SQUID = "#232F3E"
    AWS_COLOR_GRAY = "#7D8998"
    AWS_COLOR_NEBULA = "#C925D1"
    AWS_COLOR_ENDOR = "#7AA116"
    AWS_COLOR_SMILE = "#ED7100"
    AWS_COLOR_COSMOS = "#E7157B"
    AWS_COLOR_GALAXY = "#8C4FFF"
    AWS_COLOR_MARS = "#DD344C"
    AWS_COLOR_ORBIT = "#01A88D"
    
    # https://www.graphviz.org/doc/info/attrs.html
    
    GRAPH_ATTR = {
        "fontsize": "24",
        "fontcolor": AWS_FG_COLOR,
        "bgcolor": AWS_BG_COLOR,
        "ranksep": "1.0",
    }
    
    CLUSTER_ATTR = {
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
    
    NODE_ATTR = {
        "fillcolor": AWS_BG_COLOR,
        "fontcolor": AWS_FG_COLOR,
        "fontname": "Arial",
    }
    
    EDGE_ATTR = {
        "fillcolor": AWS_ARROW_COLOR,
        "color": AWS_ARROW_COLOR,
        "fontcolor": AWS_FG_COLOR,
        "labelfontcolor": AWS_FG_COLOR,
        "arrowhead": "vee",
        "arrowsize": "1.25",
        "style": "bold",
    }
    
    REGION = CLUSTER_ATTR | {"pencolor": AWS_COLOR_ORBIT, "style": "dotted"}
    AVAILABILITY_ZONE = CLUSTER_ATTR | {"pencolor": AWS_COLOR_ORBIT, "style": "dashed"}
    SECURITY_GROUP = CLUSTER_ATTR | {"pencolor": AWS_COLOR_MARS, "labeljust": "c"}
    VPC = CLUSTER_ATTR | {"pencolor": AWS_COLOR_GALAXY}
    PUBLIC_SUBNET = CLUSTER_ATTR | {"pencolor": AWS_COLOR_ENDOR}
    PRIVATE_SUBNET = CLUSTER_ATTR | {"pencolor": AWS_COLOR_ORBIT}
    GENERIC_GROUP = CLUSTER_ATTR | {
        "pencolor": AWS_COLOR_GRAY,
        "labeljust": "c",
        "style": "dashed",
    }
    ```
- When generating `with Diagram()`, add `graph_attr=GRAPH_ATTR, node_attr=NODE_ATTR, edge_attr=EDGE_ATTR` as keyword arguments.
- When generating `with Cluster()`, add `graph_attr=GENERIC_GROUP` as keyword arguments.
  - If the Cluster label contains VPC, then instead add `graph_attr=VPC`.
  - If the Cluster label contains "Availability Zone" or AZ, then instead add `graph_attr=AVAILABILITY_ZONE`.
  - If the Cluster label contains "Private Subnet", then instead add `graph_attr=PRIVATE_SUBNET`.
  - If the Cluster label contains "Public Subnet", then instead add `graph_attr=PUBLIC_SUBNET`.
  - If the Cluster label contains "Security Group", then instead add `graph_attr=SECURITY_GROUP`.
- When generating `Edge()` DO NOT add `color` or `style` keyword arguments as these come from EDGE_ATTR.
- If creating an individual Lambda function, use `LambdaFunction()`.
- Ensure that all required Python imports (such as `from diagrams import Diagram, Cluster, Edge`) are at the beginning of the `.py` file.
