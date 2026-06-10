from file_manipulation import copy_directory
from generation import generate_pages


def main():
    copy_directory(source="static", destination="public")
    generate_pages(
        content_dir_path="content",
        template_path="template.html",
        dest_dir_path="public",
    )


if __name__ == "__main__":
    main()
