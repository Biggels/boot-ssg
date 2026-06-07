import os
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def copy_directory(source="static", destination="public"):

    src_path = os.path.join(PROJECT_ROOT, source)
    if not os.path.exists(src_path):
        raise ValueError("source directory does not exist in project root")
    dest_path = os.path.join(PROJECT_ROOT, destination)
    if os.path.exists(dest_path):
        print("destination directory exists. deleting...")
        shutil.rmtree(dest_path)
    print("creating destination directory...")
    os.mkdir(dest_path)

    for item in os.listdir(src_path):
        item_src_path = os.path.join(src_path, item)
        item_dest_path = os.path.join(dest_path, item)
        if os.path.isdir(item_src_path):
            print(f"copying directory {item_src_path} to {item_dest_path}...")
            # this recursion works because item_src_path is already an absolute path
            # and os.path.join() discards other args once it hits an absolute path
            # so in the recursive call when we do e.g. os.path.join(PROJECT_ROOT, source)
            # the PROJECT_ROOT part is discarded
            # probably it would be better to make a helper function that doesn't do the top-level stuff
            # so no joining on the project root, and no checking the destination and deleting it
            # but this works
            copy_directory(source=item_src_path, destination=item_dest_path)
        else:
            print(f"copying file {item_src_path} to {item_dest_path}...")
            shutil.copy(item_src_path, item_dest_path)
