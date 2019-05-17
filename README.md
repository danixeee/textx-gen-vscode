# VS Code extension generator

Run:

```bash
textx generate example/workflow.tx -o . --target=vscode --lang-name Workflow --pattern *.wf
```

to create a `zip` archive in cwd.

Run:

```bash
textx generate example/workflow.tx -o . --target=vscode --lang-name Workflow --pattern *.wf --vsix True
```

to create a `vsix` file in cwd.
