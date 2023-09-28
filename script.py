import os
import sys
import imghdr

def list_files(directory, exclusions=[]):
    files_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclusions]
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

def display_file_content(file_path):
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

if len(sys.argv) != 2:
    print("Usage: python list_files.py /path/to/directory")
    sys.exit(1)

directory_to_explore = sys.argv[1]

if not os.path.isdir(directory_to_explore):
    print(f"Error: '{directory_to_explore}' is not a valid directory.")
    sys.exit(1)

# Liste des dossiers à exclure (tous les dossiers qui commencent par ".old" et ".git")
directories_to_exclude = [d for d in os.listdir(directory_to_explore) if d.startswith(".old")]
directories_to_exclude.append(".git")

files_list = list_files(directory_to_explore, directories_to_exclude)

for file_path in files_list:
    display_file_content(file_path)
