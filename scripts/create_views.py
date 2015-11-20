import os
from string import Template

templates_dir = "/home/himudian/Code/cheermonk/website/cheermonk/templates"
templates = ["sample_dashboard", "sample_frontend"]

project_dir = "/home/himudian/Code/cheermonk/website/cheermonk"

views_template = Template('''

@$template.route('/$url_name')
def $func_name():
    return render_template('$template$path')
''')


def list_files(template):

    outdir_path = os.path.join(project_dir, 'blueprints', template)
    outfile_path = os.path.join(outdir_path, 'views.py')
    outfile = open(outfile_path, 'w')
    outfile.seek(0)

    outfile.write("from flask import Blueprint, render_template\n\n")
    outfile.write("{0} = Blueprint('{0}', __name__, template_folder='templates')\n".format(template))

    dirname = os.path.join(templates_dir, template)
    for root, dirs, files in os.walk(dirname):
        for file in files:
            rel_dir = root.replace(dirname, '')

            file_no_ext, ext = os.path.splitext(file)
            name = '_'.join([rel_dir, file_no_ext])
            name = name.replace('/', '_').replace('-', '_')
            name = name[1:]

            path = '/'.join([rel_dir, file])

            if name == 'index':
                outfile.write(views_template.substitute(url_name='', func_name=name, path=path, template=template))
            else:
                outfile.write(views_template.substitute(url_name=name, func_name=name, path=path, template=template))

    outfile.truncate()
    outfile.close()


def main():
    for template in templates:
        list_files(template)


if __name__ == "__main__":
    main()
