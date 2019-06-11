from functools import wraps

import click
from textx import generator as _generator
from textx import language_descriptions

from .generator import generate_vscode_extension


class TextXProject:
    def __init__(
        self, name, publisher=None, version=None, repo=None, desc=None
    ):
        self.name = name.replace('_', '-')
        self.publisher = publisher or 'textX'
        self.version = version or '0.1.0'
        self.repository = repo or 'https://github.com/textX/textX-LS'
        self.description = desc or self.name

        self.languages = []
        self._load_languages()
        self.has_language = True if len(self.languages) > 0 else False

    def _is_same_project(self, project_name):
        """Compare project names replacing `-` and `_` with empty char."""
        def replace(name):
            return name.replace('-', '_').lower()
        return replace(project_name) == replace(self.name)

    def _load_languages(self):
        for lang in language_descriptions().values():
            if self._is_same_project(lang.project_name):
                self.languages.append(lang)


def generator(language, target):
    def decorator(f):
        @_generator(language, target)
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Required fields
            project_name = kwargs.get('project')
            if not project_name:
                click.echo('\nError: Missing option "--project".')
                return

            to_vsix = bool(kwargs.get('vsix'))

            lang_publisher = kwargs.get('publisher')
            lang_version = kwargs.get('version')
            lang_repo = kwargs.get('repo')
            lang_desc = kwargs.get('desc')

            project = TextXProject(project_name, lang_publisher,
                                   lang_version, lang_repo, lang_desc)
            if not project.has_language:
                click.echo('\nError: Project {} does not have any language.'
                           .format(project_name))
                return

            f(project, to_vsix, *args[1:])
        return wrapper
    return decorator


@generator('textX', 'vscode')
def vscode_gen(project, to_vsix, model, output_path=None,
               overwrite=True, debug=False):
    """Generating VS Code extension from textX grammars"""
    # TODO: Do not ignore `overwrite` and `debug` fields...
    # TODO: Allow passing --novsix argument to get zip with extension files
    generate_vscode_extension(project, model, output_path, True, to_vsix)
