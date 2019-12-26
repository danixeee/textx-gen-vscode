import platform
import shutil
import subprocess
import tempfile
from functools import partial
from os import getcwd
from os.path import abspath, dirname, join, relpath
from pathlib import Path

import jinja2
from textx import language_descriptions

from textx_gen_coloring.generators import generate_textmate_syntax

this_folder = dirname(__file__)
template_path = join(this_folder, "template")

# Load vscode template
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True,
)


def _is_same_project(project_name1, project_name2):
    """Compare projects.
    In some cases dash is converted to underscore, but the project is the same.
    """

    def _replace(name):
        return name.replace("-", "_").lower()

    return _replace(project_name1) == _replace(project_name2)


def _get_languages_by_project_name(project_name):
    """Get registered languages by project name."""
    return [
        lang
        for lang in language_descriptions().values()
        if _is_same_project(lang.project_name, project_name)
    ]


def _copy(
    project_name, publisher, version, repository, description, languages, src, dest
):
    """Populates jinja template."""
    if src.endswith("template"):
        template_rel_path = relpath(src, template_path)
        template = jinja_env.get_template(template_rel_path)
        dest = dest.replace(".template", "")
        with open(dest, "w") as f:
            f.write(
                template.render(
                    project_name=project_name,
                    publisher=publisher,
                    version=version,
                    repository=repository,
                    description=description,
                    languages=languages,
                )
            )
        return dest
    else:
        return shutil.copy2(src, dest)


def generate_vscode_extension(
    project_name,
    publisher="textX",
    version="0.1.0",
    repository="https://github.com/textX/textX-LS",
    description="textX",
    vsix=False,
    output_path="",
    skip_keywords=False,
    vsce="vsce",
):
    """Generate minimal extension from template files and given information.

    - textX language project needs to be installed before running vscode-generator
    - syntax files are generated for every language that belongs to the same project
    """
    languages = _get_languages_by_project_name(project_name)

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp = join(tmpdirname, "tmp")

        # Copy files from ./template directory while populating *.template
        shutil.copytree(
            template_path,
            tmp,
            copy_function=partial(
                _copy,
                project_name,
                publisher,
                version,
                repository,
                description,
                languages,
            ),
        )

        # Generate syntax highlighting
        for lang in languages:
            lang_name = lang.name.lower()
            lang_syntax_path = Path(tmp) / "syntaxes" / "{}.json".format(lang_name)
            lang_syntax_path.write_text(
                generate_textmate_syntax(
                    lang.metamodel, lang_name, skip_keywords=skip_keywords
                )
            )

        if not output_path:  # pragma: no cover
            output_path = getcwd()
        archive_dest = abspath(join(output_path, project_name))

        # Create installable .vsix file
        if vsix:
            subprocess.run(
                [vsce, "package", "-o", "{}.vsix".format(archive_dest)],
                cwd=tmp,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=platform.system() == "Windows",
            )
        # Create .tar file
        else:
            shutil.make_archive(archive_dest, "gztar", tmp)
