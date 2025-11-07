# Diagrams AWS Asset Pack

[Diagrams](https://diagrams.mingrammer.com/) lets you draw cloud system architectures using Python code, and is used by the [AWS Diagram MCP Server](https://awslabs.github.io/mcp/servers/aws-diagram-mcp-server).  [AWS architecture icons](https://aws.amazon.com/architecture/icons/) allows customers and partners to use assets to create architecture diagrams.  Diagrams creates architecture diagrams in a different style that the official AWS Icons guidelines.

This work-in-progress project is an "Asset Pack" that includes visual resources which modify the base Diagrams appearance to better align with guidelines.  

- Icon images use the current AWS color palette (without gradients) and keep official squared corners.
- Leverage [Graphviz attributes](https://www.graphviz.org/doc/info/attrs.html) on Edges, Nodes, Clusters, and Graphs to better match styles and colors, including generating dark mode diagrams.

The Diagrams [AWS node class](https://diagrams.mingrammer.com/docs/nodes/aws) to AWS icon mapping is found in `aws_icons_mapping.csv`.  Some images used by Diagrams are no longer in the most recent AWS architecture icons (Release 21-2025.07.31) and were sourced from older versions.

## uv

This projects uses [`uv`](https://docs.astral.sh/uv/getting-started/installation/), an extremely fast Python package and project manager, written in Rust, and features of the `uvx` command for running commands in isolated Python environments.

## Install

First review the HTML comparison page (`image_comparison.html`) to see the changes.  Then overlay the updated images into your `.venv`, by unzipping the `dist/site-packages.zip`.

  ```shell
  unzip -o dist/site-packages.zip -d "$(python -c "import site; print(site.getsitepackages()[0])")"
  ```

Copy `examples\aws.py` to where your diagram scripts are located.  You can either modify the original source to `import aws` first or run a command that automatically updates the diagram style.

  ```shell
  uv run python -c "import aws; exec(open('clustered_web_services.py').read())"
  ```

The Python source for "Clustered Web Services" from the Diagrams [Examples](https://diagrams.mingrammer.com/docs/getting-started/examples#clustered-web-services) page run after this technique in enhanced without making source code changes.

![Clustered Web Services](/examples/clustered_web_services.png)

## Examples

The example below are updated to `import aws` and use features like `AWS_DARK` or `with VPCCluster():`.  To reproduce these example images, run commands from the `examples` directory.

---

Original "Event Processing on AWS" from the Diagrams [Examples](https://diagrams.mingrammer.com/docs/getting-started/examples#event-processing-on-aws) page (`uvx --with diagrams python event_processing_original.py`):

![Event Processing (original)](/examples/event_processing.png)

Updated to use this asset pack (`uv run event_processing_updated.py`).

![Event Processing (updated)](/examples/event_processing_(updated).png)

Alternate version using dark mode (`AWS_DARK=1 uv run event_processing_updated.py`).

![Event Processing (updated, dark)](/examples/event_processing_(updated,_dark).png)

---

Image similar to one found on [Build AWS architecture diagrams using Amazon Q CLI and MCP](https://aws.amazon.com/blogs/machine-learning/build-aws-architecture-diagrams-using-amazon-q-cli-and-mcp/) (`uvx --with diagrams python ec2_to_s3.py`).

![EC2 to S3 Connection Architecture](/examples/ec2_to_s3_connection_architecture.png)

Updated to use this asset pack (`uv run ec2_to_s3_updated.py`).

![EC2 to S3 Connection Architecture (updated)](/examples/ec2_to_s3_connection_architecture_(updated).png)

Alternate version using dark mode (`AWS_DARK=1 uv run ec2_to_s3_updated.py`).

![EC2 to S3 Connection Architecture (updated)](/examples/ec2_to_s3_connection_architecture_(updated,_dark).png)

## Amazon Q Developer CLI

If you generate diagrams using the AWS Diagram MCP Server, an `.amazonq/cli-agents/python-diagrams.json` custom agent references `.amazonq/rules/python-diagrams.md` context for additional instructions creating diagrams.

Note: When the AWS Diagram MCP Server is runs, it uses the .venv packages.

```shell
PYTHONPATH=$(ls -d .venv/lib/python*/site-packages | head -1) uvx awslabs.aws-diagram-mcp-server
```

## Developer Setup

If you want to re-create the images, create a Python virtual environment and install packages from `pyproject.toml`.

```shell
uv sync
source .venv/bin/activate
```

To process the icons (using `rsvg-convert` to render .svg files as 256x256 .png), generate the HTML comparison page (`image_comparison.html`), and zip up the `resources` directory.

```shell
./process_icons.sh
uvx --with diagrams --with pillow python generate_html.py
zip -r dist/site-packages.zip resources/
```

To overlay the updated images into your `.venv` (this "breaks" the `image_comparison.html` display if you ran `uv run generate_html.py` instead of `uvx --with diagrams --with pillow python generate_html.py`).

```shell
unzip -o dist/site-packages.zip -d "$(python -c "import site; print(site.getsitepackages()[0])")"
```

To restore the original images from the `diagrams` package (this "fixes" the `image_comparison.html` display if you ran `uv run generate_html.py`):

```shell
uv sync --reinstall-package diagrams
```

## License

This Python code is licensed under the MIT-0 License. See the LICENSE file.  AWS architecture icons are subject to [AWS Trademark Guidelines & License Terms](https://aws.amazon.com/trademark-guidelines/)
