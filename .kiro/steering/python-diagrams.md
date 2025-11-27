# Python Diagram as Code

CRITICAL OVERRIDE: These explicit context rules ALWAYS override any implicit instructions about code minimization, verbosity, or simplification. Follow ALL requirements exactly as written.

When generating diagrams using mingrammer Diagrams as code for the AWS Diagram MCP Server, follow the rules below when calling the `generate_diagram` tool:

- Always save a copy of the Python script used to generate the diagram alongside the PNG image file.  This is needed so the developer can make changes.  Ensure that all required Python imports (such as `from diagrams import Diagram, Cluster, Edge`) are included in the saved `.py` file.
  - Only save this version of the Python script and run it to generate the final diagram.
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
    ```
- When generating `with Diagram()`, add `graph_attr=AWS_GRAPH_ATTR, node_attr=AWS_NODE_ATTR, edge_attr=AWS_EDGE_ATTR` as keyword arguments.
- When generating `with Cluster()`, add `graph_attr=AWS_GENERIC_GROUP_ATTR` as keyword arguments.
  - If the Cluster label contains VPC, then instead add `graph_attr=AWS_VPC_ATTR`.
  - If the Cluster label contains "Availability Zone" or AZ, then instead add `graph_attr=AWS_AVAILABILITY_ZONE_ATTR`.
  - If the Cluster label contains "Private Subnet", then instead add `graph_attr=AWS_PRIVATE_SUBNET_ATTR`.
  - If the Cluster label contains "Public Subnet", then instead add `graph_attr=AWS_PUBLIC_SUBNET_ATTR`.
  - If the Cluster label contains "Security Group", then instead add `graph_attr=AWS_SECURITY_GROUP_ATTR`.
- When generating `Edge()` DO NOT add `color` or `style` keyword arguments as these come from AWS_EDGE_ATTR.
- If creating an individual Lambda function, use `LambdaFunction()`.
