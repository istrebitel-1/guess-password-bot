# guess-password-bot

## Building project

### 1. Download

```bash
git clone git@github.com:istrebitel-1/guess-password-bot.git
```

### 2. Install dependencies

```bash
cd guess-password-bot && python3 -m venv .venv && source .venv/bin/activate
pip install -U pip setuptools
pip install .[code-quality]
```

### 3. Start the app

> Launch from project root folder

Fill env from [example file](.env.template)
Default values provided in  [settings file](./src/settings.py)

Run

```bash
python main.py
```

### Code quality

Install dependencies: `pip install .[code-quality]`  
  
[Docs: flake8](https://pypi.org/project/flake8/)  
[Docs: mypy](https://mypy.readthedocs.io/en/stable/)
[Docs: black](https://pypi.org/project/black/)  
[Docs: isort](https://pypi.org/project/isort/3.8.1/)  
[Docs: pylint](https://pypi.org/project/pylint/)

### Before merge request validation

```bash
./code_quality_check.sh
```
