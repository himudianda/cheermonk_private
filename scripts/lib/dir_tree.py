import os
import shutil


def create_dir_tree(source_folder, destination_folder, dirs_to_ignore):
    '''
        Copy the entire directory tree recursively
    '''
    for root, dirs, files in os.walk(source_folder):
        sub_path = root.replace(source_folder, "")
        dest_dir_rel_path = ''.join([destination_folder, sub_path])

        if any(item in sub_path and sub_path.startswith(item) for item in dirs_to_ignore):
            continue

        if not os.path.exists(dest_dir_rel_path):
            os.mkdir(dest_dir_rel_path)


def copy_dir_tree(source_folder, destination_folder, dirs_to_ignore, files_to_ignore):
    '''
        Copy the entire directory tree recursively
    '''
    for root, dirs, files in os.walk(source_folder):
        sub_path = root.replace(source_folder, "")
        dest_dir_rel_path = ''.join([destination_folder, sub_path])

        if any(item in sub_path and sub_path.startswith(item) for item in dirs_to_ignore):
            continue

        for filename in files:
            src_file_path = os.path.join(root, filename)
            dst_file_path = os.path.join(dest_dir_rel_path, filename)

            if any(item in dst_file_path for item in files_to_ignore):
                continue

            if os.path.exists(dst_file_path):
                if os.stat(src_file_path).st_mtime > os.stat(dst_file_path).st_mtime:
                    shutil.copy2(src_file_path, dst_file_path)
            else:
                shutil.copy2(src_file_path, dst_file_path)


def create_dir(directoy):
    if not os.path.exists(directoy):
        os.mkdir(directoy)


def delete_dir_tree(directoy):
    '''
        Delete entire directoy tree
    '''
    if os.path.exists(directoy):
        shutil.rmtree(directoy)
