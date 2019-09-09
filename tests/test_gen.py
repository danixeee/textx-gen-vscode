from click.testing import CliRunner
from textx.cli import textx


def _vscode_gen_cli(grammar_path, **kwargs):
    """Helper function to call the generator.
    kwargs is a dict in format flag: value
    - if flag is passed with one underscore, it will be converted to dash
    - if flag is passed with two underscores, it will be converted to single underscore
    """
    cmd = ["generate", "--target", "vscode", grammar_path]
    for flag, value in kwargs.items():
        flag = (
            flag.replace("__", "_") if flag.find("__") != -1 else flag.replace("_", "-")
        )
        cmd.extend(["--{}".format(flag), value])

    runner = CliRunner()
    result = runner.invoke(textx, cmd)

    return result.stdout, result.exception


def test_vscode_gen_cli_bad_args(workflow_grammar_path, tmpdir):
    output, err = _vscode_gen_cli(workflow_grammar_path, output_path=str(tmpdir))
    assert 'Error: Missing option: "--project_name".' in output
    assert err.code != 0
