import shutil
import subprocess
import tempfile
from functools import partial
from os.path import abspath, dirname, join, relpath

import jinja2

from textx import generator_for_language_target, metamodel_from_file
from textx_gen_coloring import TEXTMATE_LANG_TARGET

this_folder = dirname(__file__)
template_path = join(this_folder, 'template')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True)


textmate_gen = generator_for_language_target(*TEXTMATE_LANG_TARGET)


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


def generate_vscode_extension(lang_desc, model, output_path,
                              overwrite=False, make_vsix=False):
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdirname = '/Users/daniel/code/textX/textx-gen-vscode/testdir'
        tmp = join(tmpdirname, 'tmp')
        shutil.copytree(template_path, tmp,
                        copy_function=partial(_copy, lang_desc))
        textmate_gen(None, model, join(tmp, 'syntax.json'), **{
            'lang-name': lang_desc.name
        })

        archive_name = '{}-{}'.format(lang_desc.name, lang_desc.version)
        archive_dest = abspath(join(output_path, archive_name))

        if make_vsix:
            archive_dest += '.vsix'
            subprocess.run(['vsce', 'package', '-o', archive_dest], cwd=tmp)
        else:  # zip folder
            shutil.make_archive(archive_dest, 'zip', tmp)
