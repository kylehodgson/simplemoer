# Build the package
```python
python3 -m pip install --upgrade build
python3 -m build
```
# Upload the package
```python
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```
