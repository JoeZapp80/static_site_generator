import shutil, os, re
from markdown_blocks import markdown_to_html_node


def main():
    copy_source_to_public()
    print("!!")
    generate_content()
    print("!!")


def generate_content():
    # Create a root window (it can be hidden)
    # Get the absolute path to the directory this script is in
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up to the project root (e.g., if script is in /root/scripts/main.py, and root is one level up)
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    # Now you're solid!
    pub_path = os.path.join(project_root, "public")
    content_path = os.path.join(project_root, "content")

    def recursion_tree(content_path, pub_path):

        for item in os.listdir(content_path):
            content_path = os.path.join(content_path, item)
            pub_path = os.path.join(pub_path, item)

            if os.path.isdir(content_path):
                print("!")
                os.mkdir(pub_path)
                print(f"directory made: {pub_path}")
                # if a directory dive deeper
                recursion_tree(content_path, pub_path)

            else:
                print("?")
                extension = os.path.splitext(content_path)[1]
                print(f"ext: {extension}")
                if extension == ".md":
                    pub_path = pub_path.rsplit(".md", 1)[0] + ".html"
                    generate_page(
                        content_path, project_root + "/template.html", pub_path
                    )

                    print(f"File generated: {pub_path}")

                content_path = content_path.rsplit("/", 1)[0] + "/"
                pub_path = pub_path.rsplit("/", 1)[0] + "/"

            # Show a message box
            print(pub_path)
            content_path = content_path.rsplit("/", 1)[0] + "/"
            pub_path = pub_path.rsplit("/", 1)[0] + "/"

    recursion_tree(content_path, pub_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        contents = file.read()
    with open(template_path, "r") as file:
        template = file.read()

    html_string = markdown_to_html_node(contents).to_html()

    title = extract_title(contents)
    result = template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(result)


def extract_title(markdown):
    print(markdown)
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")


def copy_source_to_public():
    # Get the absolute path to the directory this script is in
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up to the project root (e.g., if script is in /root/scripts/main.py, and root is one level up)
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    # Now you're solid!
    pub_path = os.path.join(project_root, "public")
    static_path = os.path.join(project_root, "static")

    def create_tree(static_path, pub_path):

        for item in os.listdir(static_path):
            static_path = os.path.join(static_path, item)
            pub_path = os.path.join(pub_path, item)

            if os.path.isdir(static_path):
                os.mkdir(pub_path)
                print(f"directory made: {pub_path}")
                # if a directory dive deeper
                create_tree(static_path, pub_path)

            else:

                shutil.copy(static_path, pub_path)
                print(f"File copied: {pub_path}")
                static_path = static_path.rsplit("/", 1)[0] + "/"
                pub_path = pub_path.rsplit("/", 1)[0] + "/"

            static_path = static_path.rsplit("/", 1)[0] + "/"
            pub_path = pub_path.rsplit("/", 1)[0] + "/"

    # Delete the existing public directory (if it exists)
    if os.path.exists(pub_path):
        shutil.rmtree(pub_path)

    # Create the public directory again
    os.makedirs(pub_path)

    create_tree(static_path, pub_path)


main()
