flake8
isort .
black .

mypy src
mypy main.py

pylint src
pylint main.py
