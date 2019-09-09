from pathlib import Path

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


def test_vscode_gen_cli_targz(workflow_grammar_path, tmpdir):
    project_name = "tx-workflow"
    _, err = _vscode_gen_cli(
        workflow_grammar_path, output_path=str(tmpdir), project__name=project_name
    )

    assert err is None
    assert (Path(str(tmpdir)) / "{}.tar.gz".format(project_name)).exists()


def test_vscode_gen_cli_vsix(workflow_grammar_path, tmpdir):
    project_name = "tx-workflow"
    _, err = _vscode_gen_cli(
        workflow_grammar_path,
        output_path=str(tmpdir),
        project__name=project_name,
        vsix="True",
    )

    assert err is None
    assert (Path(str(tmpdir)) / "{}.vsix".format(project_name)).exists()


def test_vscode_gen_cli_bad_args(workflow_grammar_path):
    output, err = _vscode_gen_cli(workflow_grammar_path)
    assert 'Error: Missing option: "--project_name".' in output
    assert err.code != 0
