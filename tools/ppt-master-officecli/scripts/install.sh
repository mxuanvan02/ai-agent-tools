#!/usr/bin/env bash
set -euo pipefail

TOOL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_PATH="${SLIDE_PIPELINE_LOCK:-$TOOL_DIR/config/slide-pipeline.lock.json}"
DEFAULT_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
PREFIX="$DEFAULT_DATA_HOME/ai-agent-tools/ppt-master-officecli"
STATE_PATH="$TOOL_DIR/.state/toolchain.json"

usage() {
  cat <<'EOF'
Usage: bash scripts/install.sh [--prefix PATH] [--state PATH]

Installs pinned PPT Master, Python dependencies, and OfficeCLI without
installing optional PyMuPDF. Existing managed checkouts are never reset.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prefix)
      [[ $# -ge 2 ]] || { echo "--prefix requires a path" >&2; exit 2; }
      PREFIX="$2"; shift 2 ;;
    --state)
      [[ $# -ge 2 ]] || { echo "--state requires a path" >&2; exit 2; }
      STATE_PATH="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

for command in git python3 npm; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "Required command is missing: $command" >&2
    exit 1
  }
done

readarray -t LOCK_VALUES < <(python3 - "$LOCK_PATH" <<'PY'
import json, sys
from pathlib import Path
lock = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(lock["ppt_master"]["url"])
print(lock["ppt_master"]["revision"])
print(lock["ppt_master"]["patch"])
print(lock["ppt_master"]["patched_file"])
print(lock["ppt_master"]["patched_sha256"])
print(lock["officecli"]["package"])
print(lock["officecli"]["version"])
for dependency in lock["python"]["dependencies"]:
    print(dependency)
PY
)

PPT_URL="${LOCK_VALUES[0]}"
PPT_REVISION="${LOCK_VALUES[1]}"
PATCH_RELATIVE="${LOCK_VALUES[2]}"
PATCHED_RELATIVE="${LOCK_VALUES[3]}"
PATCHED_SHA="${LOCK_VALUES[4]}"
OFFICE_PACKAGE="${LOCK_VALUES[5]}"
OFFICE_VERSION="${LOCK_VALUES[6]}"
PYTHON_DEPENDENCIES=("${LOCK_VALUES[@]:7}")

PREFIX="$(python3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$PREFIX")"
STATE_PATH="$(python3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$STATE_PATH")"
PPT_REPO="$PREFIX/ppt-master"
VENV="$PREFIX/venv"
OFFICE_DIR="$PREFIX/officecli"
OFFICE_BIN="$OFFICE_DIR/node_modules/.bin/officecli"
PATCH_PATH="$TOOL_DIR/$PATCH_RELATIVE"
PATCHED_FILE="$PPT_REPO/$PATCHED_RELATIVE"

mkdir -p "$PREFIX"
if [[ ! -e "$PPT_REPO" ]]; then
  git clone --no-checkout "$PPT_URL" "$PPT_REPO"
  git -C "$PPT_REPO" checkout --detach "$PPT_REVISION"
elif [[ ! -d "$PPT_REPO/.git" ]]; then
  echo "Existing path is not a Git checkout: $PPT_REPO" >&2
  exit 1
fi

ACTUAL_REVISION="$(git -C "$PPT_REPO" rev-parse HEAD)"
if [[ "$ACTUAL_REVISION" != "$PPT_REVISION" ]]; then
  echo "Existing PPT Master checkout has revision $ACTUAL_REVISION; expected $PPT_REVISION." >&2
  echo "Choose another --prefix or remove the managed prefix explicitly." >&2
  exit 1
fi

actual_sha() { python3 - "$1" <<'PY'
import hashlib, sys
from pathlib import Path
path = Path(sys.argv[1])
print(hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "missing")
PY
}

CURRENT_SHA="$(actual_sha "$PATCHED_FILE")"
if [[ "$CURRENT_SHA" != "$PATCHED_SHA" ]]; then
  if git -C "$PPT_REPO" apply --unidiff-zero --check "$PATCH_PATH"; then
    git -C "$PPT_REPO" apply --unidiff-zero "$PATCH_PATH"
  else
    echo "Compatibility patch cannot be applied cleanly, and patched checksum does not match." >&2
    exit 1
  fi
fi

CURRENT_SHA="$(actual_sha "$PATCHED_FILE")"
if [[ "$CURRENT_SHA" != "$PATCHED_SHA" ]]; then
  echo "Patched file checksum mismatch: expected $PATCHED_SHA, found $CURRENT_SHA" >&2
  exit 1
fi

if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/python" -m pip install --disable-pip-version-check "${PYTHON_DEPENDENCIES[@]}"

mkdir -p "$OFFICE_DIR"
npm install --prefix "$OFFICE_DIR" --no-save --no-package-lock \
  "$OFFICE_PACKAGE@$OFFICE_VERSION"
[[ -x "$OFFICE_BIN" ]] || { echo "OfficeCLI executable was not installed: $OFFICE_BIN" >&2; exit 1; }

mkdir -p "$(dirname "$STATE_PATH")"
python3 - "$STATE_PATH" "$PREFIX" "$PPT_REPO" "$VENV/bin/python" "$OFFICE_BIN" <<'PY'
import json, sys
from pathlib import Path
state_path, prefix, repo, python, officecli = sys.argv[1:]
payload = {
    "schema": "slide-pipeline-state.v1",
    "prefix": prefix,
    "ppt_master_repo": repo,
    "ppt_master_python": python,
    "officecli_command": officecli,
}
path = Path(state_path)
path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

"$VENV/bin/python" - "$PPT_REPO" <<'PY'
import sys
from pathlib import Path
scripts = Path(sys.argv[1]) / "skills" / "ppt-master" / "scripts"
sys.path.insert(0, str(scripts))
from svg_to_pptx.pptx_package.builder import _resolve_package_target
assert _resolve_package_target("ppt/slides/slide1.xml", "../slideLayouts/slideLayout1.xml") == "ppt/slideLayouts/slideLayout1.xml"
assert _resolve_package_target("ppt/slides/slide1.xml", "/ppt/slideLayouts/slideLayout1.xml") == "ppt/slideLayouts/slideLayout1.xml"
assert _resolve_package_target("ppt/slideLayouts/slideLayout1.xml", "../slideMasters/slideMaster1.xml") == "ppt/slideMasters/slideMaster1.xml"
assert _resolve_package_target("ppt/slideLayouts/slideLayout1.xml", "/ppt/slideMasters/slideMaster1.xml") == "ppt/slideMasters/slideMaster1.xml"
print("PPT Master relationship resolver: 4/4 passed")
PY

INSTALLED_VERSION="$("$OFFICE_BIN" --version | tr -d '"\r\n')"
if [[ "${INSTALLED_VERSION#v}" != "$OFFICE_VERSION" ]]; then
  echo "OfficeCLI version mismatch: expected $OFFICE_VERSION, found $INSTALLED_VERSION" >&2
  exit 1
fi

printf 'Installed PPT Master + OfficeCLI pipeline\n  prefix: %s\n  state:  %s\n  officecli: %s\n' \
  "$PREFIX" "$STATE_PATH" "$INSTALLED_VERSION"
