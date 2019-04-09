import shutil
import subprocess
import tempfile
from functools import partial
from os import getcwd
from os.path import dirname, join, relpath

import jinja2
from textx import GeneratorDesc

this_folder = dirname(__file__)
template_path = join(this_folder, 'template')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True)


def _copy(lang, src, dest):
    """Populates jinja template."""
    if src.endswith('template'):
        template_rel_path = relpath(src, template_path)
        template = jinja_env.get_template(template_rel_path)
        dest = dest.replace('.template', '')
        with open(dest, 'w') as f:
            f.write(template.render(lang=lang))
        return dest
    else:
        return shutil.copy2(src, dest)


def generate_vscode_extension(model, output_path, overwrite):
    # Can we pass additional data?
    class Lang:
        pass
    lang = Lang()
    lang.id = 'workflow'
    lang.name = 'textx-workflow'
    lang.description = 'workflow lang'
    lang.version = '0.1.0'
    lang.publisher = 'danixeee'
    lang.repository = '-'

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp = join(tmpdirname, 'tmp')
        shutil.copytree(template_path, tmp,
                        copy_function=partial(_copy, lang))

        file_name = '{}-{}.vsix'.format(lang.name, lang.version)
        subprocess.run(['vsce', 'package'], cwd=tmp)
        vsix = join(tmpdirname, 'tmp', file_name)
        vsix_dest = join(output_path or getcwd(), file_name)
        shutil.copyfile(vsix, vsix_dest)


vscode_generator = GeneratorDesc(language='textX',
                                 target='vscode',
                                 description='VS Code extension generator',
                                 generator=generate_vscode_extension)
