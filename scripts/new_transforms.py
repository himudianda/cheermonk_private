import os
import re
import StringIO

from lib.dir_tree import create_dir_tree, copy_dir_tree, delete_dir_tree, create_dir


cur_dir = os.getcwd()
parent_dir = os.path.dirname(cur_dir)
themes_dir = os.path.join(parent_dir, "_full_backups/themes")
tmp_dest_dir = "/tmp"

METRONIC = {
    'name': "metronic",
    'dirname': "Metronic_v4.5.2",
    'original_dirname': os.path.join(themes_dir, "Metronic_v4.5.2"),
    'temp_dirname': os.path.join(tmp_dest_dir, "Metronic_v4.5.2"),
    'assets_name': "dashboard",
    'templates_name': "sample_dashboard",
    'words_to_replace': {
        'metronic': 'cheermonk',
        'Metronic': 'Cheermonk',
        'themeforest.net': 'cheermonk.com',
        'themeforest': 'cheermonk',
        'keenthemes.com': 'cheermonk.com',
        'keenthemes': 'cheermonk',
        'KeenThemes': 'Cheermonk'
    },
    'dirs_to_ignore': [
        '/_documentation', '/_resources', '/_start', '/theme_rtl',
        '/theme/admin_1', '/theme/admin_1_angularjs', '/theme/admin_1_material_design', '/theme/admin_1_rounded',
        '/theme/admin_2_angularjs', '/theme/admin_2_material_design', '/theme/admin_2_rounded',
        '/theme/admin_3', '/theme/admin_3_angularjs', '/theme/admin_3_material_design', '/theme/admin_3_rounded',
        '/theme/admin_4', '/theme/admin_4_angularjs', '/theme/admin_4_material_design', '/theme/admin_4_rounded',
        '/theme/admin_5', '/theme/admin_5_material_design', '/theme/admin_5_rounded',
        '/theme/admin_6', '/theme/admin_6_material_design', '/theme/admin_6_rounded',
        '/theme/admin_7', '/theme/admin_7_material_design', '/theme/admin_7_rounded',
        '/theme/sass', '/theme/demo'
    ],
    'files_to_ignore': [
        '/readme.txt', '/start.html', '/theme/gulpfile.js', '/theme/package.json'
    ]
}

CANVAS = {
    'name': "canvas",
    'dirname': "Canvas_v3.0.1",
    'original_dirname': os.path.join(themes_dir, "Canvas_v3.0.1"),
    'temp_dirname': os.path.join(tmp_dest_dir, "Canvas_v3.0.1"),
    'assets_name': "frontend",
    'templates_name': "sample_frontend",
    'words_to_replace': {
        'canvas': 'cheermonk',
        'Canvas': 'Cheermonk',
        'themeforest.net': 'cheermonk.com',
        'themeforest': 'cheermonk',
        'semicolonweb.com': 'cheermonk.com',
        'semicolonweb': 'cheermonk',
        'SemiColonWeb': 'Cheermonk'
    },
    'dirs_to_ignore': ['/Documentation', '/HTML-RTL'],
    'files_to_ignore': []
}

THEMES = [METRONIC, CANVAS]


def delete_old_tmp_copy(theme):
    '''
        Deletes previous copy of theme from /tmp directoy
    '''
    delete_dir_tree(theme['temp_dirname'])


def copy_theme_to_tmp(theme):
    '''
        Create a copy of the theme in /tmp directoy
    '''
    source_folder = theme['original_dirname']
    dst_folder = theme['temp_dirname']

    # Create the destination directory structure first
    create_dir_tree(source_folder, dst_folder, theme['dirs_to_ignore'])
    copy_dir_tree(source_folder, dst_folder, theme['dirs_to_ignore'], theme['files_to_ignore'])


def organize_metronic_static_assets(theme):
    src_dir = os.path.join(theme['temp_dirname'], 'theme', 'assets')
    dst_dir = os.path.join(theme['temp_dirname'], theme['assets_name'])

    # Copy over metronic static assets to new dir
    create_dir_tree(src_dir, dst_dir, [])
    copy_dir_tree(src_dir, dst_dir, [], [])

    # Remove some unwanted HTML files in assets dir
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/jqvmap/samples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/fullcalendar/demos'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/ckeditor/samples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/amstockcharts/plugins/dataloader/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'plugins/amcharts/amstockcharts/plugins/responsive/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'plugins/amcharts/amstockcharts/plugins/export/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/ammap/plugins/dataloader/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/ammap/plugins/export/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'plugins/amcharts/amcharts/plugins/dataloader/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/amcharts/plugins/responsive/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/amstockcharts/plugins/responsive/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/amstockcharts/plugins/export/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/ammap/plugins/responsive/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/amcharts/plugins/dataloader/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/amcharts/amcharts/plugins/export/examples'))
    delete_dir_tree(os.path.join(dst_dir, 'global/plugins/morris/examples'))

    # Remove old metronic static assets dir
    delete_dir_tree(src_dir)


def organize_metronic_templates(theme):
    src_dir = os.path.join(theme['temp_dirname'], 'theme', 'admin_2')
    dst_dir = os.path.join(theme['temp_dirname'], theme['templates_name'])

    # Copy over metronic templates to new dir
    create_dir_tree(src_dir, dst_dir, [])
    copy_dir_tree(src_dir, dst_dir, [], [])

    # Remove old metronic templates dir
    parent_dir = os.path.dirname(src_dir)
    delete_dir_tree(parent_dir)


def organize_canvas_static_assets(theme):
    dir_names = ['css', 'demos', 'images', 'js', 'one-page/css', 'one-page/images']

    # Create the parents directories before the child directories are created in the for
    # loop below.
    dst_assets_dir = os.path.join(theme['temp_dirname'], theme['assets_name'])
    create_dir(dst_assets_dir)
    dst_assets_dir = os.path.join(theme['temp_dirname'], theme['assets_name'], 'one-page')
    create_dir(dst_assets_dir)

    for dirname in dir_names:
        src_dir = os.path.join(theme['temp_dirname'], 'HTML', dirname)
        dst_dir = os.path.join(theme['temp_dirname'], theme['assets_name'], dirname)

        create_dir_tree(src_dir, dst_dir, [])
        copy_dir_tree(src_dir, dst_dir, [], [])


        # Remove old canvas static assets dir
        delete_dir_tree(src_dir)


def organize_canvas_templates(theme):
    src_dir = os.path.join(theme['temp_dirname'], 'HTML')
    dst_dir = os.path.join(theme['temp_dirname'], theme['templates_name'])

    # Copy over metronic templates to new dir
    create_dir_tree(src_dir, dst_dir, [])
    copy_dir_tree(src_dir, dst_dir, [], [])

    # Remove some unwanted assets dir & files in templates dir
    delete_dir_tree(os.path.join(dst_dir, 'css'))
    delete_dir_tree(os.path.join(dst_dir, 'demos'))
    delete_dir_tree(os.path.join(dst_dir, 'images'))
    delete_dir_tree(os.path.join(dst_dir, 'include'))
    delete_dir_tree(os.path.join(dst_dir, 'js'))
    delete_dir_tree(os.path.join(dst_dir, 'less'))

    delete_dir_tree(os.path.join(dst_dir, 'one-page/css'))
    delete_dir_tree(os.path.join(dst_dir, 'one-page/images'))
    delete_dir_tree(os.path.join(dst_dir, 'one-page/include'))

    # Remove old canvas templates dir
    delete_dir_tree(src_dir)


def organize_theme_dirs(theme):
    # Move all static_assets to static_assets dir
    # More all templates to templates dir
    if theme['name'] == "metronic":
        organize_metronic_static_assets(theme)
        organize_metronic_templates(theme)
    elif theme['name'] == "canvas":
        organize_canvas_static_assets(theme)
        organize_canvas_templates(theme)

    # Remove all other directories


def rename_sensitive_words(theme):
    '''
        Remove all theme specific words & urls
    '''
    sensitive_words = theme['words_to_replace']
    pattern = re.compile(r'(' + '|'.join(sensitive_words.keys()) + r')')

    for root, dirs, files in os.walk(theme['temp_dirname']):
        for filename in files:
            full_file_path = os.path.join(root, filename)

            # Rename sensitive words within files
            with open(full_file_path, 'r+') as infile:
                data = infile.read()
                result = pattern.sub(lambda x: sensitive_words[x.group()], data)

                # http://stackoverflow.com/questions/6648493/open-file-for-both-reading-and-writing
                # Overwrite the file
                infile.seek(0)
                infile.write(result)
                infile.truncate()

            # Rename directory/filenames to remove sensitive words
            if any(word in filename for word in sensitive_words):
                new_filename = pattern.sub(lambda x: sensitive_words[x.group()], filename)

                new_file_path = os.path.join(root, new_filename)
                os.rename(full_file_path, new_file_path)


def flaskify_metronic_theme(theme):
    metronic_assets_regex = re.compile('../assets/(.*?)"')
    metronic_templates_regex = re.compile('href="(.*?).html"')

    # Only flaskify template files - no static assets should be flaskified.
    theme_template_dir = os.path.join(theme['temp_dirname'], theme['templates_name'])

    for root, dirs, files in os.walk(theme_template_dir):
        for filename in files:
            full_file_path = '/'.join([root, filename])

            with open(full_file_path, 'r+') as infile:
                outfile = StringIO.StringIO()
                for line in infile.readlines():

                    # Apply asset specific regex & transformation
                    m = metronic_assets_regex.search(line)
                    if m:
                        asset_dir = m.group(1)
                        line = re.sub(
                            '"../assets/(.*?)"',
                            '"{{ url_for(\'static\', filename=\'dashboard/'+asset_dir+'\') }}"',
                            line
                        )

                    # Apply template specific regex & transformation
                    m = metronic_templates_regex.search(line)
                    if m:
                        endpoint = m.group(1)
                        line = re.sub(
                            '"(.*?).html"',
                            '"{{ url_for(\'sample_dashboard.'+endpoint+'\') }}"',
                            line
                        )

                    outfile.write(line)

                # Overwrite the input file now
                infile.seek(0)
                infile.write(outfile.getvalue())
                infile.truncate()


def flaskify(theme):
    if theme['name'] == "metronic":
        flaskify_metronic_theme(theme)


def main():
    for theme in THEMES:
        delete_old_tmp_copy(theme)
        copy_theme_to_tmp(theme)
        organize_theme_dirs(theme)
        rename_sensitive_words(theme)
        flaskify(theme)

if __name__ == "__main__":
    main()
