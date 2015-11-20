import os

from lib.dir_tree import create_dir_tree, copy_dir_tree, delete_dir_tree


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
    pass


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


def main():
    for theme in THEMES:
        delete_old_tmp_copy(theme)
        copy_theme_to_tmp(theme)
        organize_theme_dirs(theme)


if __name__ == "__main__":
    main()
