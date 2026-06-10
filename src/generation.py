import os
import re

from transformations import markdown_to_html_node

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_title(markdown: str) -> str:
    if not markdown:
        raise ValueError("Markdown cannot be empty/None")
    match = re.search(r"^# (.+)$", markdown, re.MULTILINE)
    if not match:
        raise ValueError("No h1 found")
    return match.group(1)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:

    from_path = os.path.join(PROJECT_ROOT, from_path)
    if not os.path.exists(from_path):
        raise ValueError("from_path does not exist in project root")

    template_path = os.path.join(PROJECT_ROOT, template_path)
    if not os.path.exists(template_path):
        raise ValueError("template_path does not exist in project root")

    dest_path = os.path.join(PROJECT_ROOT, dest_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    with open(dest_path, "w") as f:
        f.write(template)
