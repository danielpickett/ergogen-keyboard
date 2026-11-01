# Pickett46 wireless split keyboard

A 46-key MX hot-swap keyboard with one nice!nano v2 per half and ZMK firmware.
The original Ergogen switch centers, rotations and 1.5u thumb positions are
preserved. Left and right have separate, fully routed two-layer PCBs.

## Fabrication files

- [Left JLCPCB ZIP](fabrication/pickett46-left-jlcpcb.zip)
- [Right JLCPCB ZIP](fabrication/pickett46-right-jlcpcb.zip)
- [Ordering details](docs/FABRICATION.md)
- [BOM](docs/BOM.csv) and [assembly instructions](docs/ASSEMBLY.md)
- [ZMK configuration, flashing and pin mapping](docs/FIRMWARE.md)

Both boards pass KiCad **9.0.2** DRC with **zero violations and zero unconnected
items**, with no DRC exclusions. The ZIPs also pass independent Gerber parsing,
layer/drill-count checks and source/hash checks. Both left/right firmware UF2s
were compiled successfully in Codex Cloud. These are digitally validated
fabrication outputs; a physical prototype has not been assembled or tested.

| Check | Left | Right |
|---|---:|---:|
| Keys / diodes | 23 / 23 | 23 / 23 |
| Copper layers | 2 | 2 |
| DRC violations | 0 | 0 |
| Unconnected items | 0 | 0 |
| Plated / non-plated drill hits | 59 / 119 | 59 / 119 |
| ZMK UF2 build | Pass | Pass |

## Editable sources and evidence

`hardware/left.kicad_pro` and `hardware/right.kicad_pro` open the production
boards in KiCad. All footprints are embedded in the PCB files; no external
footprint library is needed to edit or fabricate them. The adjacent `.kicad_dru`
files define manufacturing constraints and must stay beside the boards.

`config.yaml` is the active Ergogen layout. `footprints/` contains the custom
controller, reset and SOD-123 diode generators. `config-mine.yaml` is an unused
historical experiment. `config/` contains ZMK files; `firmware/` contains the
compiled images. `validation/` contains DRC, electrical/layout, mechanical,
Gerber and firmware evidence. `fabrication/manifest.json` records source and
ZIP SHA-256 hashes. `docs/previews/` shows actual exported copper and silk; the
bottom-layer images are shown through the board from the front, not mirrored
assembly views. `docs/plates/` contains the original-layout DXF switch cutouts.

## Reproduce or edit

Use Node.js with Ergogen 4.1.0, KiCad 9 CLI and KiCad's system Python `pcbnew` API.
All development and validation for this revision ran in Codex Cloud.

```sh
npm install
npm run build                 # unrouted scaffolds in output/pcbs
/usr/bin/python3 scripts/prepare_pcbs.py  # optional DSNs in output/kicad
bash scripts/validate.sh       # checks the committed routed hardware files
bash scripts/fabricate.sh      # validates, then exports both ZIPs
```

Ergogen generates placement and net assignments, **not finished copper**. The
committed `hardware/` boards additionally contain routing, antenna keepouts,
cleaned silkscreen and fabrication rules. The preparation script writes only
to `output/`, so it cannot silently replace the routed boards. After a layout
change, carry it into the production boards, reroute and rerun fabrication.
Specctra conversion rounds positions to 0.1 µm; the layout audit permits only
that rounding relative to the original layout saved from commit `7c6f7c1`.

For independent ZIP/mechanical checks, install
`scripts/requirements-validation.txt` in a Python virtual environment, then run:

```sh
python scripts/audit_exports.py
```

This parses the actual ZIPs and regenerates their SVG previews. KiCad's
Excellon output may produce a parser warning about G90 appearing after the
header; it is accepted and the drill coordinates and counts are checked.

Routing used Freerouting 2.1.0 plus final clearance-aware trace completion and
KiCad DRC cleanup. DRC clearance limits were not relaxed to make the boards pass.
