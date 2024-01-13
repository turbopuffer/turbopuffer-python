# Release Build Instructions

To build and publish the PyPI package:

1. Set up `~/.pypirc` with PyPI api token.
2. Install `build` and `twine` python packages
    ```sh
    $ python -m pip install --upgrade build
    $ python -m pip install --upgrade twine
    ```
3. Remove existing output
    ```sh
    $ rm -rf dist/
    ```
4. Build new package
    ```sh
    $ python -m build
    ```
5. Upload release
    ```sh
    $ python -m twine upload dist/*
    ```
