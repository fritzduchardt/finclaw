#!/bin/bash

OS_FINCLAW_SCRIPT_DIR="$(dirname -- "${BASH_SOURCE[0]:-${0}}")"

activate_finclaw_env() {
  source "$OS_FINCLAW_SCRIPT_DIR"/.venv/bin/activate
}

claw() {
  activate_finclaw_env
  PYTHONPATH=$OS_FINCLAW_SCRIPT_DIR python3 -m src.finclaw.cli "$@"
}
