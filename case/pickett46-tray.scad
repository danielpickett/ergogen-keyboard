// Pickett46 open tray fit prototype, dimensions in millimeters.
// PCB outline from hardware/left.kicad_pcb.
// The right PCB perimeter is its reflection. The outlines share a 134 mm width.
side = "left"; // [left, right]
board_clearance = 0.45;
wall_thickness = 2.4;
floor_thickness = 2.4;
under_board_height = 6;
board_thickness = 1.6;
ledge_overlap = 0.8;
ledge_height = 2;

pcb = [
    [0, 0],
    [134, 0],
    [134, -66.23],
    [133.996771, -66.235768],
    [110.593632, -102.273443],
    [0, -62]
];

module perimeter(distance) {
    offset(delta = distance) polygon(pcb);
}

module tray() {
    seat_z = floor_thickness + under_board_height;

    difference() {
        linear_extrude(height = seat_z + board_thickness)
            perimeter(board_clearance + wall_thickness);

        // Keep the central cavity clear for sockets and solder joints.
        translate([0, 0, floor_thickness])
            linear_extrude(height = seat_z + board_thickness)
                perimeter(board_clearance);
    }

    translate([0, 0, seat_z - ledge_height])
        linear_extrude(height = ledge_height)
            difference() {
                // Overlap the wall to give the ledge a solid connection.
                perimeter(board_clearance + wall_thickness / 2);
                perimeter(-ledge_overlap);
            }
}

if (side == "right")
    translate([134, 0, 0]) mirror([1, 0, 0]) tray();
else
    tray();
