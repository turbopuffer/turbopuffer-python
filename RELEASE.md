# Release Build Instructions

To build and publish the PyPI package:

1. `python -m pip install --upgrade build`
1. `python -m pip install --upgrade twine`
1. `rm -rf dist/`
2. `python -m build`
3. `python -m twine upload dist/*`