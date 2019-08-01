# Human-Traffic-Count
Human Traffic Count (HTC)

#Sample Vscode workspace setting
```javascript
{
    "python.autoComplete.extraPaths": [
        "${workspaceRoot}/addons",
        "D:\\odoo source from git\\odoo\\addons",
        "C:\\Program Files (x86)\\Odoo 12.0e\\server\\odoo"
    ],
    //"python.linting.pylintPath": "optional: path to python use if you have environment path",
    "python.linting.enabled": true,
    //load the pylint_odoo
    "python.linting.pylintArgs": [
        "--load-plugins",
        "pylint_odoo"
    ],
    "python.formatting.provider": "yapf",
    //"python.formatting.yapfPath": "optional: path to python use if you have environment path",
    // "python.linting.pep8Path": "optional: path to python use if you have environment path",
    "python.linting.pep8Enabled": true,
    // add this auto-save option so the pylint will sow errors while editing otherwise
    //it will only show the errors on file save
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 500,
    // The following will hide the compiled file in the editor/ add other file to hide them from editor
    "files.exclude": {
        "**/*.pyc": true
    },
    "editor.formatOnSave": true
}
```

#Sample Launch.json for vscode
```javascript
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python",
            "type": "python",
            "request": "launch",
            "stopOnEntry": false,
            "pythonPath": "your pyton.exe path",
            "program": "your odoo bin path",
            //your odoo configuration file path
            "args": [
                "-c${workspaceRoot}\\odoo.conf"
            ],
            "cwd": "${workspaceRoot}",
        }
    ],
}
``
