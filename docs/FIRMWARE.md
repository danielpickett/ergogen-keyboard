# ZMK firmware

`firmware/pickett46-left.uf2` and `firmware/pickett46-right.uf2` were built in
Codex Cloud for **nice!nano v2**. Left is central; right is peripheral. The
configuration pins ZMK commit `4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85` and uses
Zephyr SDK 0.17.4 (GNU Arm 12.2.0). Both complete build logs are in `validation/`.
The minimal libc setting avoids the SDK picolibc/Zephyr locking type conflict.

Double-press reset on each installed controller to enter its UF2 bootloader,
then copy the matching UF2 to that controller's USB drive. Pair the left half
with the host over Bluetooth; the right connects to the left. Do not flash the
left image onto both halves. For a controller previously used in another split
keyboard, clear its saved settings/bonding before pairing the new pair; use
ZMK's `settings_reset` shield build for the same nice!nano target, then reflash
the appropriate keyboard UF2. No reset image is needed for factory-fresh boards.

The keymap is a 46-key adaptation of the owner's prior QMK layout for the
`dpickett_split_refined2`. It preserves its QWERTY base layer, symbol/navigation
layer, number layer, and media/function/reset layer. The three dedicated Escape
keys present on that older keyboard are not present on this 46-key layout.
The keymap has exactly 46 bindings per layer. Idle sleep is enabled after 15
minutes.

## Wiring

| Signal | nRF GPIO | Controller pad | ZMK matrix |
|---|---|---|---|
| P029 | P0.29 | 19 | top row 0 |
| P002 | P0.02 | 18 | home row 1 |
| P115 | P1.15 | 17 | bottom row 2 |
| P113 | P1.13 | 16 | thumb row 3 |
| P006 | P0.06 | 1 | outer column 0 |
| P008 | P0.08 | 2 | pinky column 1 |
| P017 | P0.17 | 5 | ring column 2 |
| P020 | P0.20 | 6 | middle column 3 |
| P022 | P0.22 | 7 | index column 4 |
| P024 | P0.24 | 8 | inner column 5 |

Both PCBs use the same electrical mapping. The transform offsets right-half
columns by 6 and reverses their display order. Thumb positions use columns 1–5;
there is no thumb key at column 0. Diode cathodes connect to rows, so scan
polarity is `col2row`. GPIO assignments were checked against the pinned ZMK
nice!nano `arduino_pro_micro_pins.dtsi` and all 46 PCB switch/diode pairs.

## Rebuild

The GitHub Actions workflow builds both targets from `build.yaml`. Locally in a
Linux/cloud build environment with west, Zephyr SDK and the normal ZMK build
requirements installed, initialize a workspace from `config/west.yml`, run
`west update`, then build from that workspace:

```sh
west build -s zmk/app -d build/left -b nice_nano@2.0.0/nrf52840/zmk -- \
  -DSHIELD=pickett46_left -DZMK_CONFIG=/absolute/path/to/ergogen-keyboard/config
west build -s zmk/app -d build/right -b nice_nano@2.0.0/nrf52840/zmk -- \
  -DSHIELD=pickett46_right -DZMK_CONFIG=/absolute/path/to/ergogen-keyboard/config
```

The successful builds validate configuration and compilation, not physical
key scanning, radio performance or charging behavior.
