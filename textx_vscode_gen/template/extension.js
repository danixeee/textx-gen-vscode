const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const textxExtension = vscode.extensions.getExtension("textX.textX");
  if (textxExtension && !textxExtension.isActive) { textxExtension.activate(); }
}

// this method is called when your extension is deactivated
function deactivate() { }

module.exports = {
  activate,
  deactivate
}
