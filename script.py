import os
import sys
import argparse
import imghdr

def list_files(directory, exclusions=[], tree_exclusions=[]):
    files_list = []
    for root, dirs, files in os.walk(directory):
        if any(excl in root for excl in tree_exclusions):
            continue
        dirs[:] = [d for d in dirs if d not in exclusions and d not in tree_exclusions]
        files = [f for f in files if f not in tree_exclusions]
        level = root.replace(directory, '').count(os.sep)
        prefix = '-' * 4 * (level)
        print(f'{prefix}[{os.path.basename(root)}/]')
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)
            print(f'{prefix} |- {file}')
    return files_list

def is_image(file_path):
    valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']
    return imghdr.what(file_path) in valid_image_extensions

def is_svg(file_path):
    return file_path.lower().endswith('.svg')

def display_file_content(file_path, extensions_to_skip=[]):
    file_extension = file_path.split('.')[-1]
    if file_extension in extensions_to_skip:
        print(f'Skipping {file_extension} file: {file_path}')
        return

    if is_image(file_path) or is_svg(file_path):
        print(f'Skipping image/SVG file: {file_path}')
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f'\nContents of {file_path}:\n')
                print(content)
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
                print(f'\nContents of {file_path} (encoded in latin-1):\n')
                print(content)

def parse_arguments():
    parser = argparse.ArgumentParser(description='List files in a directory')
    parser.add_argument('directory', help='Path to the directory to explore')
    parser.add_argument('--tree', action='store_true', help='Display only the tree structure of the files')
    parser.add_argument('--skip', nargs='*', default=[], help='Extensions to skip')
    parser.add_argument('--skip-tree', nargs='*', default=[], help='File/Dir names to skip in tree listing')
    return parser.parse_args()

args = parse_arguments()

directory_to_explore = args.directory
extensions_to_skip = args.skip
tree_exclusions = args.skip_tree

if not os.path.isdir(directory_to_explore):
    print(f"Error: '{directory_to_explore}' is not a valid directory.")
    sys.exit(1)

directories_to_exclude = [d for d in os.listdir(directory_to_explore) if d.startswith(".old")]
directories_to_exclude.append(".git")

if args.tree:
    list_files(directory_to_explore, directories_to_exclude, tree_exclusions)
else:
    files_list = list_files(directory_to_explore, directories_to_exclude)
    for file_path in files_list:
        display_file_content(file_path, extensions_to_skip)