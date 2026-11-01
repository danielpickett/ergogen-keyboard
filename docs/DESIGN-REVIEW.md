# Electrical and mechanical review

Original baseline: repository commit `7c6f7c1`. The original left scaffold had
107 DRC violations and 172 unconnected items. It used soldered MX footprints,
combo diodes with pads crossing the thumb-edge cut, two parallel battery
connectors per half, and a bottom-mounted right reset switch.

This revision enables Ergogen's Kailh MX socket footprint on both halves. Each
switch has two bottom SMD contacts and five non-plated holes: stem, two locating
posts, and two socket/switch-contact openings. Switches mount from the front;
sockets mount underneath. No reversible socket variant is used.

The replacement diode footprint uses the KiCad SOD-123 land pattern (1.4 × 1.2 mm
pads at ±1.65 mm), on the bottom only. It is shifted below each switch to remain
inside the board and clear of the hot-swap socket body. The cathode bar identifies
pad 1, which connects to a row; pad 2 connects to its switch. Firmware uses
`col2row`. Every switch/diode/controller net assignment is checked independently
by `scripts/audit_board.py`; KiCad checks copper connectivity and clearance.

Each nice!nano uses 24 through-hole socket pads at 2.54 mm pitch, with 15.24 mm
between rows. Its components face up, USB toward the straight top edge, RAW/B+
at top right. The original three extra pin holes were removed because the
matrix does not use the underside auxiliary pins. Controller power goes from
JST1 pad 1 through T1 to RAW/B+; JST1 pad 2 goes to GND. VCC is the controller's
regulated output and does not connect to the battery. B1 momentarily joins RST
to GND. The unselected T1 throw is deliberately unconnected. Both reset buttons
are mounted on the front. The duplicate parallel battery connectors are removed.

The antenna keepouts span 12 × 8 mm between the controller socket rows at the
antenna end, on both copper layers. They prohibit traces, pads, vias and copper
fills. Keep external conductive materials clear too. Module height, battery
placement and RF range require assembly testing.

The original 46 switch positions/rotations remain within the 0.1 µm Specctra
rounding tolerance. A nominal keycap-body model uses 18.25 × 18.25 mm on 1u keys
and 18.25 × 27.75 mm at S21. It gives 0.75 mm minimum keycap separation and
1.485 mm clearance between keycaps and the nice!nano module body. JST1 is outside
the adjacent cap envelopes. The PCB outlines and plate cutouts preserve the
original geometry; there are no added case or mounting-hole assumptions.

Final evidence is in `validation/`: zero DRC violations, zero unconnected items,
no ignored violations; all 46 electrical paths checked; Gerber layer and drill
counts matched to sources; both firmware builds pass. The design has not had a
physical prototype or functional charging/RF validation.

Pin mapping reference: the pinned ZMK source's
`app/module/boards/nicekeyboards/nice_nano/arduino_pro_micro_pins.dtsi`.
Controller orientation was also cross-checked against ceoloide's
[`mcu_nice_nano.js`](https://github.com/ceoloide/ergogen-footprints/blob/main/mcu_nice_nano.js),
which specifies RAW/B+ at top right for component-side-up mounting.
