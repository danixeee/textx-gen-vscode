from functools import wraps

from textx import generator as _generator

from .generator import generate_vscode_extension


class LanguageDesc:
    def __init__(self, name, file_pattern, publisher=None,
                 version=None, repo=None, desc=None):
        self.name = name.lower()
        self.lang_file_ext = file_pattern.split('.')[-1]
        self.publisher = publisher or 'textX'
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

            lang_file_pattern = kwargs.get('pattern')
            if not lang_file_pattern:
                raise Exception('Language file extension is required (--pattern *.wf).')  # noqa

            to_vsix = bool(kwargs.get('vsix'))

            lang_publisher = kwargs.get('publisher')
            lang_version = kwargs.get('version')
            lang_repo = kwargs.get('repo')
            lang_desc = kwargs.get('desc')

            lang_desc = LanguageDesc(lang_name, lang_file_pattern, lang_publisher,
                                     lang_version, lang_repo, lang_desc)

            f(lang_desc, to_vsix, *args[1:])
        return wrapper
    return decorator


@generator('textX', 'vscode')
def vscode_gen(lang_desc, to_vsix, model, output_path=None,
               overwrite=True, debug=False):
    """Generating VS Code extension from textX grammars"""
    # TODO: Do not ignore `overwrite` and `debug` fields...
    # TODO: Allow passing --novsix argument to get zip with extension files
    # TODO: --intall argument to install vsix
    generate_vscode_extension(lang_desc, model, output_path, True, to_vsix)
