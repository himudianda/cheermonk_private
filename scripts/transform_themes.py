import os
import shutil
import re

cur_dir = os.getcwd()
parent_dir = os.path.dirname(cur_dir)
themes_dir = os.path.join(parent_dir, "_full_backups/themes")
tmp_dest_dir = "/tmp"

METRONIC = {
    'name': "metronic",
    'dirname': "Metronic_v4.5.2",
    'original_dirname': '/'.join([themes_dir, "Metronic_v4.5.2"]),
    'words_to_replace': {
        'metronic': 'cheermonk',
        'Metronic': 'Cheermonk',
        'themeforest.net': 'cheermonk.com',
        'themeforest': 'cheermonk',
        'keenthemes.com': 'cheermonk.com',
        'keenthemes': 'cheermonk',
        'KeenThemes': 'Cheermonk'
    }
}

CANVAS = {
    'name': "canvas",
    'dirname': "Canvas_v3.0.1",
    'original_dirname': '/'.join([themes_dir, "Canvas_v3.0.1"]),
    'words_to_replace': {
        'canvas': 'cheermonk',
        'Canvas': 'Cheermonk',
        'themeforest.net': 'cheermonk.com',
        'themeforest': 'cheermonk',
        'semicolonweb.com': 'cheermonk.com',
        'semicolonweb': 'cheermonk',
        'SemiColonWeb': 'Cheermonk'
    }
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

        if not os.path.exists(statics_folder):
            os.mkdir(statics_folder)

        dirs_to_move = ['HTML/css', 'HTML/demos', 'HTML/images', 'HTML/include', 'HTML/js', 'HTML/less']
        for directory in dirs_to_move:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.move(full_dirname, statics_folder)

        # Move pending template files into templates/sample_frontend dir
        files_to_move = [
            'frontend/include/ajax/portfolio-single-gallery.html',
            'frontend/include/ajax/portfolio-single-image.html',
            'frontend/include/ajax/portfolio-single-thumbs.html',
            'frontend/include/ajax/portfolio-single-video.html',
            'frontend/include/ajax/shop-item.html'
        ]
        new_dirname = os.path.join(dst_folder, 'HTML/include')
        if not os.path.exists(new_dirname):
            os.mkdir(new_dirname)
        new_dirname = os.path.join(new_dirname, 'ajax')
        if not os.path.exists(new_dirname):
            os.mkdir(new_dirname)

        for file in files_to_move:
            full_filename = os.path.join(dst_folder, file)
            shutil.move(full_filename, new_dirname)

        # Move pending asset files into static dir
        dirs_to_move = ['HTML/one-page/css', 'HTML/one-page/images', 'HTML/one-page/include']
        files_to_move = ['HTML/one-page/onepage.css', 'HTML/style.css', 'HTML/style-import.css', 'HTML/style.less']
        statics_one_page_folder = os.path.join(dst_folder, "frontend/one-page")

        if not os.path.exists(statics_one_page_folder):
            os.mkdir(statics_one_page_folder)
        for directory in dirs_to_move:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.move(full_dirname, statics_one_page_folder)
        for file in files_to_move:
            full_filename = os.path.join(dst_folder, file)
            if "one-page" in file:
                shutil.move(full_filename, statics_one_page_folder)
            else:
                shutil.move(full_filename, statics_folder)

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
        files_to_move = ['theme/admin_2/favicon.ico']
        for file in files_to_move:
            full_filename = os.path.join(dst_folder, file)
            shutil.move(full_filename, '/'.join([dst_folder, 'theme/assets']))
        for directory in dirs_to_move:
            full_dirname = os.path.join(dst_folder, directory)
            shutil.move(full_dirname, dst_folder)
        shutil.rmtree(os.path.join(dst_folder, 'theme'))

        # Rename the directories
        os.rename(os.path.join(dst_folder, 'admin_2'), os.path.join(dst_folder, 'sample_dashboard'))
        os.rename(os.path.join(dst_folder, 'assets'), os.path.join(dst_folder, 'dashboard'))


def delete_old_tmp_copy(theme):
    shutil.rmtree(theme['temp_dirname'])


def do_renaming(theme):
    sensitive_words = theme['words_to_replace']
    pattern = re.compile(r'(' + '|'.join(sensitive_words.keys()) + r')')

    dirname = theme['temp_dirname']
    for root, dirs, files in os.walk(dirname):
        for filename in files:
            full_file_path = '/'.join([root, filename])

            # Rename the contents within the file
            with open(full_file_path, 'r+') as infile:
                data = infile.read()
                result = pattern.sub(lambda x: sensitive_words[x.group()], data)

                # http://stackoverflow.com/questions/6648493/open-file-for-both-reading-and-writing
                infile.seek(0)
                infile.write(result)
                infile.truncate()

                '''
                for line in infile:

                    # http://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python
                    if any(word in line for word in sensitive_words):

                        # http://stackoverflow.com/questions/2400504/easiest-way-to-replace-a-string-using-a-dictionary-of-replacements
                        pattern = re.compile(r'\b(' + '|'.join(sensitive_words.keys()) + r')\b')
                        result = pattern.sub(lambda x: sensitive_words[x.group()], line)

                        print result
                '''

            # Rename the directory/filenames
            if any(word in filename for word in sensitive_words):
                new_filename = pattern.sub(lambda x: sensitive_words[x.group()], filename)
                new_file_path = '/'.join([root, new_filename])
                os.rename(full_file_path, new_file_path)


def flaskify(theme):

    metronic_assets_regex = re.compile('../assets/(.*?)"')
    metronic_templates_regex = re.compile('href="(.*?).html"')
    canvas_assets_regex = re.compile('href="(.*?)"')
    canvas_images_regex = re.compile('img src="(.*?)"')
    canvas_templates_regex = re.compile('href="(.*?).html"')

    templates_root_dir = '/home/himudian/Code/cheermonk/website/cheermonk/templates'
    if not os.path.exists(templates_root_dir):
        os.mkdir(templates_root_dir)

    if not os.path.exists('/'.join([templates_root_dir, 'sample_dashboard'])):
        os.mkdir('/'.join([templates_root_dir, 'sample_dashboard']))

    if not os.path.exists('/'.join([templates_root_dir, 'sample_frontend'])):
        os.mkdir('/'.join([templates_root_dir, 'sample_frontend']))

    if not os.path.exists('/'.join([templates_root_dir, 'sample_frontend/one-page'])):
        os.mkdir('/'.join([templates_root_dir, 'sample_frontend/one-page']))

    if not os.path.exists('/'.join([templates_root_dir, 'sample_frontend/include'])):
        os.mkdir('/'.join([templates_root_dir, 'sample_frontend/include']))

    if not os.path.exists('/'.join([templates_root_dir, 'sample_frontend/include/ajax'])):
        os.mkdir('/'.join([templates_root_dir, 'sample_frontend/include/ajax']))

    static_root_dir = '/home/himudian/Code/cheermonk/website/cheermonk/static'
    if not os.path.exists(static_root_dir):
        os.mkdir(static_root_dir)

    if not os.path.exists('/'.join([static_root_dir, 'dashboard'])):
        os.mkdir('/'.join([static_root_dir, 'dashboard']))

    if not os.path.exists('/'.join([static_root_dir, 'frontend'])):
        os.mkdir('/'.join([static_root_dir, 'frontend']))

    dirname = theme['temp_dirname']
    for root, dirs, files in os.walk(dirname):

        # Ignore all template directories
        #if '/sample_' in root:
        #    continue

        # Create directories that dont exist
        out_dir_path = root.replace(theme['temp_dirname'], '')
        out_dir_path = ''.join([static_root_dir, out_dir_path])

        if not os.path.exists(out_dir_path):
            os.mkdir(out_dir_path)

        for filename in files:

            # All static files ARE NOT to be Flaskified.
            # Only copy it to the prject
            if '.html' not in filename:

                full_file_path = '/'.join([root, filename])
                with open(full_file_path, 'r') as infile:
                    out_file_path = '/'.join([out_dir_path, filename])

                    outfile = open(out_file_path, 'w')
                    outfile.write(infile.read())
                    outfile.close()

                # Dont Flaskify static files
                continue

            full_file_path = '/'.join([root, filename])
            with open(full_file_path, 'r') as infile:
                if theme['name'] == 'metronic':
                    out_file_path = '/'.join([templates_root_dir, 'sample_dashboard', filename])
                    outfile = open(out_file_path, 'w')

                    for line in infile.readlines():
                        m = metronic_assets_regex.search(line)
                        if m:
                            asset_dir = m.group(1)
                            line = re.sub(
                                '"../assets/(.*?)"',
                                '"{{ url_for(\'static\', filename=\'dashboard/'+asset_dir+'\') }}"',
                                line
                            )

                        m = metronic_templates_regex.search(line)
                        if m:
                            endpoint = m.group(1)
                            line = re.sub(
                                '"(.*?).html"',
                                '"{{ url_for(\'sample_dashboard.'+endpoint+'\') }}"',
                                line
                            )

                        outfile.write(line)
                    outfile.close()

                elif theme['name'] == 'canvas':

                    if 'one-page' in full_file_path:
                        out_file_path = '/'.join([templates_root_dir, 'sample_frontend/one-page', filename])
                    elif 'include/ajax' in full_file_path:
                        out_file_path = '/'.join([templates_root_dir, 'sample_frontend/include/ajax', filename])
                    else:
                        out_file_path = '/'.join([templates_root_dir, 'sample_frontend', filename])
                    outfile = open(out_file_path, 'w')

                    for line in infile.readlines():
                        if 'http' in line:
                            continue

                        m = canvas_assets_regex.search(line)
                        if m and '.html' not in m.group(1):
                            asset_dir = m.group(1)

                            if asset_dir == '#':
                                line = re.sub(
                                    '"#"',
                                    '"{{ url_for(\'static\', filename=\''+asset_dir+'\') }}"',
                                    line
                                )
                            else:
                                if 'one-page' in full_file_path:
                                    if '../' in asset_dir:
                                        asset_dir = asset_dir.strip('../')
                                        line = re.sub(
                                            '"../(.*?)"',
                                            '"{{ url_for(\'static\', filename=\'frontend/'+asset_dir+'\') }}"',
                                            line
                                        )
                                    else:
                                        line = re.sub(
                                            'href="(.*?)"',
                                            'href="{{ url_for(\'static\', filename=\'frontend/one-page/'+asset_dir+'\') }}"',
                                            line
                                        )

                                        m = canvas_images_regex.search(line)
                                        if m:
                                            img_dir = m.group(1)
                                            line = re.sub(
                                                'src="(.*?)"',
                                                'src="{{ url_for(\'static\', filename=\'frontend/one-page/'+img_dir+'\') }}"',
                                                line
                                            )
                                else:
                                    line = re.sub(
                                        'href="(.*?)"',
                                        'href="{{ url_for(\'static\', filename=\'frontend/'+asset_dir+'\') }}"',
                                        line
                                    )
                                    m = canvas_images_regex.search(line)
                                    if m:
                                        img_dir = m.group(1)
                                        line = re.sub(
                                            'src="(.*?)"',
                                            'src="{{ url_for(\'static\', filename=\'frontend/'+img_dir+'\') }}"',
                                            line
                                        )

                        m = canvas_templates_regex.search(line)
                        if m:
                            endpoint = m.group(1)
                            endpoint = endpoint.replace('/', '_')
                            line = re.sub(
                                '"(.*?).html"',
                                '"{{ url_for(\'sample_frontend.'+endpoint+'\') }}"',
                                line
                            )

                            m = canvas_images_regex.search(line)
                            if m:
                                img_dir = m.group(1)
                                line = re.sub(
                                    'img src="(.*?)"',
                                    'img src="{{ url_for(\'static\', filename=\'frontend/'+img_dir+'\') }}"',
                                    line
                                )

                        outfile.write(line)
                    outfile.close()


def main():
    for theme in THEMES:
        theme['temp_dirname'] = '/'.join([tmp_dest_dir, theme['dirname']])

        delete_old_tmp_copy(theme)
        copy_theme_to_tmp(theme)
        organize_dirs(theme)

        do_renaming(theme)

        flaskify(theme)

if __name__ == "__main__":
    main()
