# VS Code Extension Generator for textX Languages

A _textX_ generator which outputs simple, installable _VS Code_ extension from a registered _textX_ language project.

It is used primary by [textX-LS](https://github.com/textX/textX-LS) project when generating and installing _textX_ languages.

## CLI Examples

Generate a _VS Code_ extension for `tx_workflow` project packaged in archive:

```bash
textx generate examples/workflow/tx_workflow/workflow.tx -o . --target=vscode --project_name tx-workflow
```

Generate a _VS Code_ extension for `tx_workflow` project packaged in installable _vsix_ format:

```bash
textx generate examples/workflow/tx_workflow/workflow.tx -o . --target=vscode --project_name tx-workflow --vsix True
```

## Other Notes

- textX language project should be registrated in order generator to find it by passed _project name_
- path to the grammar (`examples/workflow/tx_workflow/workflow.tx`) is not used for now, but idea is to be able to create project from it
