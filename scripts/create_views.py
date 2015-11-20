import os
from string import Template

templates_dir = "/home/himudian/Code/cheermonk/website/cheermonk/templates"
templates = ["sample_dashboard", "sample_frontend"]

views_template = Template('''
@sample_dashboard.route('/$name')
def $name():
    return render_template('$template/$path')
''')


def list_files(template):
    dirname = os.path.join(templates_dir, template)
    for root, dirs, files in os.walk(dirname):
        print root, dirname

        for file in files:
            name = root.replace(dirname, '')

            file_no_ext, ext = os.path.splitext(file)
            name = '_'.join([name, file_no_ext])

            name = name.replace('/', '_')
            name = name.replace('-', '_')

            name = name[1:]

            new_name = root.replace(dirname, '')
            new_name = '/'.join([new_name, file])
            path = ''.join([template, new_name])

            print views_template.substitute(name=name, path=path, template=template)


def main():
    for template in templates:
        list_files(template)


if __name__ == "__main__":
    main()
