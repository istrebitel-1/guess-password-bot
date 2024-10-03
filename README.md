# confecence-bot-backend

## Building project

### 1. Download from gitlab

```bash
git clone git@gitlab.raftds.com:python-shared/fastapi-app-template.git

OR

git clone https://gitlab.raftds.com/python-shared/fastapi-app-template.git
```

### 2. Install dependencies

```bash
cd fastapi-app-template && python3 -m venv .venv && source .venv/bin/activate
pip install -U pip setuptools
pip install .[code-quality,testing]
```

### 3. Start the app

> Launch from project root folder

Fill env from [example file](./backend/config/environment/env.sh.template)
Default values provided in  [settings file](./backend/settings.py)

Run

Up postgres from `docker-compose up -d` or provide `.env` file with your credentials

```bash
uvicorn main:app
```

or with hot reload

```bash
uvicorn main:app --reload
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

## Release process

Prerequisites: you should have maintainer or owner access to the repository

1. Create a new branch named release-*.*.* from main
2. Go to CI/CD page and click "Run pipeline" button
3. Wait for the pipeline to finish
