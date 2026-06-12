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


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:

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
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages(content_dir_path, template_path, dest_dir_path, basepath):
    content_dir_path = os.path.join(PROJECT_ROOT, content_dir_path)
    if not content_dir_path:
        raise ValueError("content directory does not exist in project root")
    template_path = os.path.join(PROJECT_ROOT, template_path)
    if not template_path:
        raise ValueError("template file does not exist in project root")
    dest_dir_path = os.path.join(PROJECT_ROOT, dest_dir_path)

    for item in os.listdir(content_dir_path):
        item_content_path = os.path.join(content_dir_path, item)
        item_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_content_path):
            if item_content_path.endswith(".md"):
                generate_page(
                    from_path=item_content_path,
                    template_path=template_path,
                    dest_path=item_dest_path[:-2] + "html",
                    basepath=basepath,
                )
        else:
            generate_pages(
                content_dir_path=item_content_path,
                template_path=template_path,
                dest_dir_path=item_dest_path,
                basepath=basepath,
            )
