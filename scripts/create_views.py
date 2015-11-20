import os
from string import Template

templates_dir = "/home/himudian/Code/cheermonk/website/cheermonk/templates"
templates = ["sample_dashboard", "sample_frontend"]

views_template = Template('''
@sample_dashboard.route('/$name')
def $name():
    return render_template('$template$path')
''')


def list_files(template):
    dirname = os.path.join(templates_dir, template)
    for root, dirs, files in os.walk(dirname):
        for file in files:
            rel_dir = root.replace(dirname, '')

            file_no_ext, ext = os.path.splitext(file)
            name = '_'.join([rel_dir, file_no_ext])
            name = name.replace('/', '_').replace('-', '_')
            name = name[1:]

            path = '/'.join([rel_dir, file])

            print views_template.substitute(name=name, path=path, template=template)


def main():
    for template in templates:
        list_files(template)


if __name__ == "__main__":
    main()
