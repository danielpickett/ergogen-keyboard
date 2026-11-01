#!/usr/bin/env bash
# Fail closed: do not export fabrication packages unless both boards pass.
set -euo pipefail
cd "$(dirname "$0")/.."
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp/pickett46-cache}"
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-/tmp/pickett46-config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-/tmp/pickett46-data}"
bash scripts/validate.sh
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
for side in left right; do
    mkdir -p "$stage/$side"
    kicad-cli pcb export gerbers "hardware/$side.kicad_pcb" -o "$stage/$side/" \
        -l F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts --subtract-soldermask
    kicad-cli pcb export drill "hardware/$side.kicad_pcb" -o "$stage/$side/" \
        --format excellon --drill-origin absolute --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th
 done
python3 scripts/package_fabrication.py "$stage"
