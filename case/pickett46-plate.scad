// Pickett46 MX switch plate fit prototype, dimensions in millimeters.
// Use the canonical switch layout in docs/plates.
side = "left"; // [left, right]
plate_thickness = 1.5;

controller_clearance = 1;

// DXF uses KiCad X and negated Y. MCU1 is at (214.5,122) on
// the left and (255.5,122) on the right, rotated -90 degrees.
// Open the notch to the top and inner edges for USB-C access.
module controller_notch() {
    controller_x = side == "right" ? 255.5 : 214.5;
    inner_edge_x = side == "right" ? 245.5 : 224.5;
    y_min = -122 - 15.24 - controller_clearance;
    y_max = -102.5 + 1;
    x_min = side == "right" ? inner_edge_x - 1
                            : controller_x - 8.89 - controller_clearance;
    x_max = side == "right" ? controller_x + 8.89 + controller_clearance
                            : inner_edge_x + 1;

    translate([x_min, y_min]) square([x_max - x_min, y_max - y_min]);
}

linear_extrude(height = plate_thickness)
    difference() {
        import(str("../docs/plates/", side, "-switch-plate.dxf"));
        controller_notch();
    }
