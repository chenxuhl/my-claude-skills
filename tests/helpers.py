"""Shared test helpers: load the dash-named scripts as importable modules."""

import importlib.util
import shutil
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
_TMP_BASE = Path(__file__).resolve().parent / "_tmp"


def load_script(name: str, filename: str):
    path = SCRIPTS_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@contextmanager
def workspace_tmp():
    """Temporary directory inside the workspace, created via Path.mkdir.

    (tempfile.mkdtemp is avoided: the sandbox refuses writes inside
    directories it creates.)
    """
    _TMP_BASE.mkdir(exist_ok=True)
    path = _TMP_BASE / uuid.uuid4().hex
    path.mkdir()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


