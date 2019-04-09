const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const textxExtension = extensions.getExtension("textX.textX");
  if (textxExtension && !textxExtension.isActive) { textxExtension.activate(); }
}

module.exports = {
  activate,
  deactivate
}
