# Validation record

All checks ran in Codex Cloud. Production sources are the two boards in
`hardware/`; fabrication ZIPs are linked to those files by SHA-256 manifest.

- KiCad 9.0.2: **0 DRC violations, 0 unconnected items** on each board. No ignored
  violations or relaxed clearance exceptions. Text and JSON reports included.
- Electrical audit: 23 MX sockets, 23 SOD-123 diodes, one controller, one battery
  connector, reset and power switch per half; all pin/net assignments checked.
- Layout: all 46 centers/rotations match the original within 0.1 µm export
  rounding. Nominal cap models have no overlap; 0.75 mm minimum cap separation,
  1.485 mm minimum controller-to-cap separation.
- Gerbonara 1.6.3 independently parses both ZIPs. Seven expected Gerber layers,
  two drill files, 59 plated and 119 non-plated drill hits per half. Every drill
  center and diameter matches the PCB source within 0.001 mm. Copper is present
  on both layers. ZIP CRCs and source/output hashes pass.
- Exported copper/silk previews were inspected. Antenna copper keepouts, separate
  masks, MX contact holes, diode pads and continuous outlines are present.
- ZMK left and right compile and link successfully for nice!nano v2. UF2s and
  successful build logs included; detailed binary hashes in firmware-builds.json.

The baseline commit is `7c6f7c1`; `original-layout.json` was extracted before
modification. The production generator uses Ergogen 4.1.0. Routing used
Freerouting 2.1.0, with final clearance-aware routing and KiCad cleanup.

These checks support bare-PCB fabrication. They do not establish physical socket
fit, key travel, switch-plate retention, RF range, charging performance, or
battery/case fit. Those need prototype assembly. A schematic/ERC report is not
provided: this is an Ergogen PCB-first design, with net assignments independently
audited against the firmware mapping instead.
