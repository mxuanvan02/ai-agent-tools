"""Make the sibling src/ directory importable so tests can `import humanize` etc.
Keeps CI commands plain (`python -m pytest tests/...`) without packaging config."""
import pathlib
import sys

_SRC = pathlib.Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
