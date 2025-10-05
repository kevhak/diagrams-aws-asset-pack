import csv
import os
import site

from PIL import Image, UnidentifiedImageError

html = """<!DOCTYPE html>
<html>
<head>
    <title>Diagrams to AWS Icons Comparison</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
        img { max-width: 64px; max-height: 64px; }
        .not-found { color: #999; font-style: italic; }
    </style>
</head>
<body>
    <h1>AWS Icons Comparison</h1>
    <table>
        <thead>
            <tr>
                <th>Diagrams Image Reference</th>
                <th>Diagrams Resource Icon</th>
                <th>Official AWS Icon</th>
                <th>Updated Resource Icon</th>
            </tr>
        </thead>
        <tbody>
"""


def get_image_dims(path):
    if path.endswith(".svg"):
        if path.endswith("_32.svg"):
            return "32x32"
        elif path.endswith("_48.svg"):
            return "48x48"
        elif path.endswith("_64.svg"):
            return "64x64"
        return "64x64"
    if os.path.exists(path):
        try:
            with Image.open(path) as img:
                return f"{img.width}x{img.height}"
        except (OSError, UnidentifiedImageError):
            pass
    return "0x0"


with open("aws_icons_mapping.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        module, class_name, diagrams_file, aws_file = row
        module_path = module.replace("aws.", "")

        html += f'''            <tr>
                <td>{module}.{class_name}</td>
                <td><img src="{site.getsitepackages()[0]}/resources/aws/{module_path}/{diagrams_file}" alt="{diagrams_file}" onerror="this.style.display='none'"><br>{get_image_dims(f"{site.getsitepackages()[0]}/resources/aws/{module_path}/{diagrams_file}")}</td>
                <td>'''

        if aws_file == "NOT_FOUND":
            html += '<span class="not-found">NOT_FOUND</span>'
        else:
            html += f'<img src="assets/{aws_file}" alt="{aws_file}" onerror="this.style.display=\'none\'"><br>{get_image_dims(f"assets/{aws_file}")}'

        html += "</td>\n                "
        if aws_file == "NOT_FOUND":
            html += "<td>&nbsp;</span></td>"
        else:
            html += f'<td><img src="resources/aws/{module_path}/{diagrams_file}" alt="{diagrams_file}" onerror="this.style.display=\'none\'"><br>{get_image_dims(f"resources/aws/{module_path}/{diagrams_file}")}</td>'

        html += "            </tr>\n"

html += """        </tbody>
    </table>
</body>
</html>"""

with open("image_comparison.html", "w") as f:
    f.write(html)

print("Generated image_comparison.html")
