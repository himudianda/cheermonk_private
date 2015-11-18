import os
import shutil

cur_dir = os.getcwd()
parent_dir = os.path.dirname(cur_dir)
themes_dir = os.path.join(parent_dir, "_full_backups/themes")
tmp_dest_dir = "/tmp"

METRONIC = {
    'name': "metronic",
    'dirname': "Metronic_v4.5.2",
    'original_dirname': '/'.join([themes_dir, "Metronic_v4.5.2"])
}

CANVAS = {
    'name': "canvas",
    'dirname': "Canvas_v3.0.1",
    'original_dirname': '/'.join([themes_dir, "Canvas_v3.0.1"])
}

THEMES = [METRONIC, CANVAS]


# Libraries
def copyrecursively(source_folder, destination_folder):
    '''
        Copy the entire directory tree recursively
    '''
    for root, dirs, files in os.walk(source_folder):

        src_path = root
        dest_rel_path = src_path.replace(source_folder, "")
        dst_path = ''.join([destination_folder, dest_rel_path])

        if not os.path.exists(dst_path):
            os.mkdir(dst_path)

        for filename in files:
            src_file_path = '/'.join([src_path, filename])
            dst_file_path = '/'.join([dst_path, filename])

            if os.path.exists(dst_file_path):
                if os.stat(src_file_path).st_mtime > os.stat(dst_file_path).st_mtime:
                    shutil.copy2(src_file_path, dst_file_path)
            else:
                shutil.copy2(src_file_path, dst_file_path)


def copy_theme_to_tmp(theme):
    source_folder = theme['original_dirname']
    dst_folder = theme['temp_dirname']
    copyrecursively(source_folder, dst_folder)


def organize_dirs(theme):
    if theme['name'] == "canvas":
        dst_folder = theme['temp_dirname']

        # Remove unwanted files & directories
        dirs_to_delete = ['Documentation', 'HTML-RTL']
        for directory in dirs_to_delete:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.rmtree(full_dirname)

        # Move stuff to the correct location
        statics_folder = os.path.join(dst_folder, "frontend")
        os.mkdir(statics_folder)

        dirs_to_move = ['HTML/css', 'HTML/demos', 'HTML/images', 'HTML/include', 'HTML/js', 'HTML/less']
        for directory in dirs_to_move:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.move(full_dirname, statics_folder)

        dirs_to_move = ['HTML/one-page/css', 'HTML/one-page/images', 'HTML/one-page/include']
        statics_one_page_folder = os.path.join(dst_folder, "frontend/one-page")
        os.mkdir(statics_one_page_folder)
        for directory in dirs_to_move:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.move(full_dirname, statics_one_page_folder)

        # Rename the directories
        os.rename(os.path.join(dst_folder, 'HTML'), os.path.join(dst_folder, 'sample_frontend'))

    elif theme['name'] == "metronic":
        dst_folder = theme['temp_dirname']

        # Remove unwanted files & directories
        dirs_to_delete = ['_documentation', '_resources', '_start', 'theme_rtl']
        files_to_delete = ['readme.txt', 'start.html']
        for directory in dirs_to_delete:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.rmtree(full_dirname)
        for file in files_to_delete:
            full_filename = os.path.join(dst_folder, file)
            os.remove(full_filename)

        # Move stuff to the correct location
        dirs_to_move = ['theme/admin_2', 'theme/assets']
        for directory in dirs_to_move:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.move(full_dirname, dst_folder)
        shutil.rmtree(os.path.join(dst_folder, 'theme'))

        # Rename the directories
        os.rename(os.path.join(dst_folder, 'admin_2'), os.path.join(dst_folder, 'sample_dashboard'))
        os.rename(os.path.join(dst_folder, 'assets'), os.path.join(dst_folder, 'dashboard'))


def delete_old_tmp_copy(theme):
    shutil.rmtree(theme['temp_dirname'])


def main():
    for theme in THEMES:
        theme['temp_dirname'] = '/'.join([tmp_dest_dir, theme['dirname']])

        delete_old_tmp_copy(theme)
        copy_theme_to_tmp(theme)
        organize_dirs(theme)


if __name__ == "__main__":
    main()
