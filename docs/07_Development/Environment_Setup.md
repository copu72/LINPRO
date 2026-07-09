# Configuración del Entorno — LINPRO

**Versión:** 1.0  
**Fecha:** 2026-07-09  

## Requisitos

| Herramienta | Versión mínima | Notas                        |
|-------------|----------------|------------------------------|
| Python      | 3.11           | No usar versiones inferiores.|
| Git         | 2.40+          | Control de versiones.        |

## Pasos de instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/organizacion/linpro.git
cd linpro
```

### 2. Crear y activar entorno virtual

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt   # Dependencias de desarrollo
```

### 4. Instalar pre-commit hooks

```bash
pre-commit install
```

Los hooks ejecutan automáticamente Ruff, mypy y chequeos de formato antes de cada commit.

## Configuración de VS Code

### Extensiones recomendadas

| Extensión          | ID                                               |
|--------------------|--------------------------------------------------|
| Python             | ms-python.python                                |
| Pylance            | ms-python.vscode-pylance                        |
| Ruff               | charliermarsh.ruff                              |
| GitLens            | eamodio.gitlens                                 |
| Markdown Preview   | yzhang.markdown-all-in-one                      |

### Configuración recomendada (`.vscode/settings.json`)

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    },
    "ruff.lint.run": "onSave",
    "ruff.format.args": ["--line-length=100"],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true
}
```

## Verificación

```bash
python -c "import linpro; print(linpro.__version__)"
pytest tests/unit/ -x
```