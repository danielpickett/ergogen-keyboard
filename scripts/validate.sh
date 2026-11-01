#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp/pickett46-cache}"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/tmp/pickett46-config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-/tmp/pickett46-data}"
mkdir -p "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" validation
/usr/bin/python3 scripts/audit_board.py
for side in left right; do
    kicad-cli pcb drc "hardware/$side.kicad_pcb" --format json --exit-code-violations -o "validation/$side-drc.json"
    kicad-cli pcb drc "hardware/$side.kicad_pcb" --exit-code-violations -o "validation/$side-drc.txt"
done
python3 - <<'PY'
import json
for side in ['left', 'right']:
    r=json.load(open(f'validation/{side}-drc.json'))
    assert not r['violations'] and not r['unconnected_items'] and not r['schematic_parity'], side
print('PASS: both PCBs have zero DRC violations and zero unconnected items.')
PY
