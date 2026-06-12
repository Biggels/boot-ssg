import sys

from file_manipulation import copy_directory
from generation import generate_pages


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_directory(source="static", destination="docs")
    generate_pages(
        content_dir_path="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath,
    )


if __name__ == "__main__":
    main()
