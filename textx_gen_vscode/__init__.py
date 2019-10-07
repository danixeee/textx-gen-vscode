import sys

import click
from textx import generator

from .generators import generate_vscode_extension


@generator("textX", "vscode")
def vscode_gen(
    metamodel,
    model,
    output_path="",
    overwrite=False,
    debug=False,
    project_name=None,
    publisher="textX",
    version="0.1.0",
    repository="https://github.com/textX/textX-LS",
    description="textX",
    vsix=False,
    skip_keywords=False,
    vsce="vsce",
):
    """Generating VS Code extension for installed textX projects."""
    if not project_name:
        click.echo('\nError: Missing option: "--project_name".')
        sys.exit(1)

    generate_vscode_extension(
        project_name,
        publisher,
        version,
        repository,
        description,
        vsix,
        output_path,
        skip_keywords,
        vsce,
    )
