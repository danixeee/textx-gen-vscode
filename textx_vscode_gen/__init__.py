from functools import wraps
from os import getcwd

from textx import generator as _generator

from .generator import generate_vscode_extension


class LanguageDesc:
    def __init__(self, name, lang_file_ext, publisher=None, version=None, repo=None, desc=None):  # noqa
        self.name = name
        self.lang_file_ext = lang_file_ext
        self.publisher = publisher or 'missing-publisher'
        self.version = version or '0.1.0'
        self.repository = repo or 'Missing repository URL.'
        self.description = desc or self.name


def generator(language, target):
    def decorator(f):
        @_generator(language, target)
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Required fields
            lang_name = kwargs.get('lang-name')
            if not lang_name:
                raise Exception('Language name is required (--lang-name Workflow).')  # noqa

            lang_file_ext = kwargs.get('file-ext')
            if not lang_file_ext:
                raise Exception('Language file extension is required (--file-ext wf).')  # noqa

            lang_publisher = kwargs.get('publisher')
            lang_version = kwargs.get('version')
            lang_repo = kwargs.get('repo')
            lang_desc = kwargs.get('desc')

            lang_desc = LanguageDesc(lang_name, lang_file_ext, lang_publisher,
                                     lang_version, lang_repo, lang_desc)

            f(lang_desc, *args[1:])
        return wrapper
    return decorator


@generator('textX', 'vscode')
def vscode_gen(lang_desc, model, output_path=getcwd(), overwrite=True, debug=False):  # noqa
    """Generating VS Code extension from textX grammars"""
    # TODO: Do not ignore `overwrite` and `debug` fields...
    # TODO: Allow passing --novsix argument to get zip with extension files
    # TODO: Think - maybe it makes more sense to generate extension for registered language # noqa
    generate_vscode_extension(lang_desc, model, output_path, True)
