# Assembly and first power-up

The left and right PCBs are different, with 23 keys each. Fit all switches from the
front. Kailh sockets and all SOD-123 diodes go on the **back**. Controllers,
battery connectors, reset buttons and slide switches go on the **front**.

1. Solder D1–D23: the stripe on the 1N4148W body faces **pad 1 / cathode / row**,
   identified by the silkscreen bar. Pad 2 is the anode and connects to its switch.
   Use SOD-123, not visually similar SOD-323 or SOD-123F parts.
2. Solder the 23 Kailh MX sockets flat against the back. Support each socket from
   below when inserting a switch. These are MX sockets, not Choc sockets.
3. Fit JST1, T1 and B1. JST1 **pad 1 is battery positive**, pad 2 is GND. Commercial
   battery leads do not have a universal polarity: measure the actual connector
   before plugging it in. Do not connect two batteries or an inter-half power cable.
4. Fit two 12-pin controller socket rows, 15.24 mm apart. Each nice!nano v2 goes
   component-side up, USB toward the straight top edge. RAW/B+ is the top-right
   controller pin viewed from the front, with USB at the top. Match the printed
   pin labels. Do not install an ordinary Pro Micro or a controller face down.
5. Before installing controllers/batteries, meter for no short from RAW, VCC or
   battery positive to GND. T1's common is RAW; only one throw connects to battery
   positive. Verify continuity in ON and isolation in OFF. B1 shorts RST to GND
   only while pressed. A switch closure connects a column to a diode anode.
6. Flash the matching left/right UF2 over USB, then fit protected single-cell
   LiPo batteries. The nice!nano handles charging; do not use a separate external
   charger at the same time. Turning T1 off isolates battery positive from the
   controller, so USB cannot charge that battery while off. USB can still power
   the controller with T1 off.
7. Test all 46 keys and both layers before closing a case. Left is the BLE central;
   right pairs to it. Test wired USB on the left, wireless host operation, split
   reconnect, reset, sleep/wake and battery charging.

Use a switch plate for hot-swap retention. The PCB has no mounting holes; design
case/plate retention around its perimeter. Allow at least 3 mm clear space below
socket bodies, plus solder and case tolerances. Keep the LiPo insulated from
pads and leads. Keep metal, batteries and conductive case features away from the
controller antenna end and the marked copper keepout, including below the PCB.
Use socket height sufficient to avoid contact between the controller and carrier.

The 46 original switch centers and rotations are unchanged. Each half uses 22
1u caps and one lengthwise 1.5u cap at S21. The checked 18.25 mm / 27.75 mm cap-body
model has 0.75 mm minimum clearance; larger skirt dimensions need separate review.
The supplied plate outlines are geometric cutouts, not a tested enclosure design.

Digital fabrication checks do not substitute for testing the assembled keyboard.
No physical prototype, RF range test, charging test or socket insertion test has
been performed in this cloud environment.
