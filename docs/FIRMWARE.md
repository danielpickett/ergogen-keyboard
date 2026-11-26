# ZMK firmware

Both halves use **nice!nano v2**. Left is the ZMK split central and handles
host pairing and keymap actions. Right is the peripheral and sends key
positions to the left. The original build logs in `validation/` describe the
Codex Cloud builds with Zephyr SDK 0.17.4 (GNU Arm 12.2.0). Use the GitHub Actions
run for the commit you intend to flash when selecting a new UF2.

Double-press reset on each installed controller to enter its UF2 bootloader,
then copy the matching UF2 to that controller's USB drive. Pair the left half
with the host over Bluetooth; the right connects to the left. Do not flash the
left image onto both halves. For a controller previously used in another split
keyboard, clear its saved settings/bonding before pairing the new pair; use
ZMK's `settings_reset` shield build for the same nice!nano target, then reflash
the appropriate keyboard UF2. Routine keymap updates use the keyboard UF2 and
preserve host and split bonds. `settings_reset` erases those bonds.

The keymap is a 46-key adaptation of the owner's prior QMK layout for the
`dpickett_split_refined2`. It preserves its QWERTY base layer, symbol/navigation
layer, number layer, and media/function/reset layer. The three dedicated Escape
keys present on that older keyboard are not present on this 46-key layout.
The keymap has exactly 46 bindings per layer. Idle sleep is enabled after 15
minutes.

## Working Bluetooth baseline

The left diagnostic build from `97a3498` passed fresh MacBook pairing with the
controller installed in the left PCB, running on battery with USB unplugged.
Profile 0 retained the iPhone bond, profile 1 paired with the MacBook, and
switching between them worked. Both halves had already passed typing on the
iPhone. [Build run and merged `firmware` archive](https://github.com/danielpickett/ergogen-keyboard/actions/runs/45747277541)

The tested left file in the archive is `pickett46-left-diagnostic.uf2`. Its
SHA-256 is `e0e67865086d5423982bbce7c6efa0b1b49cf9efafd2a1dd518eb952419effb6`.
Keep a copy labeled with the commit for rollback. A generic local filename like
`pickett46-left.uf2` can still point to an older build. Use `shasum -a 256 <file>`
on macOS to identify a local copy of the tested image.

For keymap-only builds, keep the [ZMK pin](../config/west.yml), the nice!nano
v2 target, and the [firmware settings](../config/pickett46.conf) from this
baseline. These include minimal libc, the 16384-byte malloc arena and 8192-byte
heap pool from `958c629`, the internal RC low-frequency clock, and experimental
BLE connection handling. Test changes to those settings separately from keymap
edits.

## Routine keymap updates

1. Edit [`config/pickett46.keymap`](../config/pickett46.keymap). Keep 46 bindings
   per layer and preserve the Bluetooth combo and profile bindings unless you
   are deliberately moving them.
2. Find the successful **Build ZMK firmware** run for your exact commit. Download
   its merged **firmware** artifact and extract `pickett46-left-diagnostic.uf2`
   for a like-for-like update with USB logging. The run page also provides the
   regular left image for testing a build without USB logging.
3. Double-tap reset and flash the left UF2 to the left half. For a bindings-only
   update, the right half can keep its installed firmware. Build and flash the
   matching pair when changing split transport, matrix mapping, or board support.
4. Unplug USB and power the keyboard from its batteries. Verify that both halves
   type, switch between the saved iPhone and MacBook profiles, and power-cycle
   the left half to check reconnection. For a fresh-pairing test, use a spare
   profile and an unpaired host so the two working bonds stay available.

### Bluetooth shortcuts

From the base layer, press the two far-left keys in the top and home rows
within 50 ms of each other and hold both. The combo uses positions `0` and `12`
and activates the Bluetooth layer. While holding both, tap the key below.

| Key | Action |
|---|---|
| Q | Select profile 0 (iPhone) |
| W | Select profile 1 (MacBook) |
| E / R / T | Select profiles 2 / 3 / 4 |
| B | Clear the selected host profile |

If W types `@`, the numbers layer handled the press. Check the flashed artifact
first, then release both layer keys and retry the combo. To check which host is
active, type a normal key after releasing the combo and see where it arrives.
When deliberately clearing a profile, also forget Pickett46 on that host before
pairing again. [ZMK Bluetooth behavior](https://zmk.dev/docs/keymaps/behaviors/bluetooth)

### If pairing regresses

Keep the existing bonds and start with an installed, battery-only test. If the
regression appears after an update, flash the saved working left UF2 and repeat
under the same conditions. The first USB capture showed `bt_crypto: Failed to
compute MAC -141` and a security failure. Later Mac and iPhone USB captures
showed repeated `0x08` link timeouts with the left controller installed. The
controller paired while bare on USB, and the assembled keyboard subsequently
paired on battery using a spare profile. The cause of the installed USB timeouts
was never isolated. For further diagnosis, compare one variable at a time and
use the diagnostic image to capture USB logs.

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
