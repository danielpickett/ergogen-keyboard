# JLCPCB ordering

Upload **one ZIP per order/design**:

- `fabrication/pickett46-left-jlcpcb.zip`
- `fabrication/pickett46-right-jlcpcb.zip`

Select two copper layers, FR4, **1.6 mm** thickness, 1 oz copper, and lead-free HASL
or ENIG. Mask color is optional. Each board's nominal outline is approximately
**134.00 × 102.273 mm**. These are separate left/right designs, not a reversible
board and not a panel. Order equal quantities of both halves. Standard JLCPCB
minimum order quantity may exceed one pair.

Each ZIP contains exactly seven Gerbers: front/back copper, front/back solder
mask, front/back silkscreen, and the board outline; plus separate plated and
non-plated Excellon drill files. Copper and drill exports use the same absolute
origin, millimeters, without mirroring. Paste layers and placement files are not
needed for bare-PCB fabrication. This is a hand-assembly package, not a JLCPCB
component assembly order.

The routing uses 0.25 mm signal traces and 0.60/0.30 mm through-vias. The included
KiCad rules enforce 0.20 mm minimum copper clearance and track width, 0.50 mm
copper-to-edge clearance, 0.15 mm annular ring, and 0.25 mm hole-to-hole clearance.
The two-layer stack has no internal copper. Antenna rule areas prohibit copper
and vias beneath the controller antenna ends.

`fabrication/manifest.json` binds the ZIPs and their individual files to the PCB
source, rule and DRC report hashes. `validation/` contains the KiCad 9.0.2 DRC
reports and electrical/layout audit. Export is fail-closed: `bash
scripts/fabricate.sh` runs those checks before producing either ZIP. The checked-in
routed `hardware/*.kicad_pcb` files are the manufacturing sources; running Ergogen
alone produces **unrouted scaffolds**, never replacement fabrication boards.

Review the JLCPCB uploader's layer detection and drill preview before ordering.
The digital design is checked; physical assembly, RF range and charging have not
been prototype-tested.
