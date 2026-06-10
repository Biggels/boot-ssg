from file_manipulation import copy_directory
from generation import generate_page


def main():
    copy_directory(source="static", destination="public")
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html",
    )


if __name__ == "__main__":
    main()
