# Generate unit test coverage report

Run from src folder

```bat
python -m pytest --cov="." --cov-config "tests\\.coveragerc" --cov-report html
```