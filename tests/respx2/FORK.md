# HTTPX2 test support

This is a test-only adaptation of [RESPX 0.22.0](https://github.com/lundberg/respx/tree/0.22.0),
distributed under its original BSD 3-Clause license in LICENSE.md.
It is excluded from SDK wheels.

Changes from upstream:

- Imports and transport patch targets use `httpx2` and `httpcore2`.
- Absolute RESPX imports point to `tests.respx2`.
- The pytest plugin is registered explicitly by `tests/conftest.py`.

The fixture and marker retain their `respx_mock` and `respx` names.
No process-wide HTTPX aliases are installed, so applications can still use legacy HTTPX independently.

To update, start from an upstream RESPX release, retain its license, reapply the import and transport
target changes, and run the generated SDK's client tests and `tests/test_respx2.py`.
Keep this directory in the generator templates in sync with generated SDKs.
