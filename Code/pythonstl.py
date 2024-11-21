from stl import mesh
import numpy as np
import trimesh

# Enclosure dimensions (in mm) based on Arduino Uno Rev 4 specs
BOARD_WIDTH = 68.6
BOARD_LENGTH = 53.4
BOARD_HEIGHT = 13.0
THICKNESS = 2.0
CLEARANCE = 1.0
SCREW_HOLE_RADIUS = 1.7
SCREW_HOLE_SPACING = [(3.2, 3.2), (3.2, 49.5), (64.4, 3.2), (64.4, 49.5)]

# Port positions (in mm) based on Arduino Uno Rev 4 specs
USB_PORT_POSITION = (0.0, 15.0)  # USB port location along the short side
USB_PORT_SIZE = (12.0, 8.0)
DC_JACK_POSITION = (0.0, 35.0)  # DC jack location along the short side
DC_JACK_SIZE = (10.0, 12.0)

# Generate the base of the enclosure using trimesh
def arduino_enclosure_base():
    base_width = BOARD_WIDTH + 2 * CLEARANCE + 2 * THICKNESS
    base_length = BOARD_LENGTH + 2 * CLEARANCE + 2 * THICKNESS
    base_height = BOARD_HEIGHT + THICKNESS

    # Create base box
    base = trimesh.creation.box(extents=[base_width, base_length, base_height])
    base.apply_translation([base_width / 2, base_length / 2, base_height / 2])

    # Create inner cutout
    inner_cutout = trimesh.creation.box(extents=[BOARD_WIDTH, BOARD_LENGTH, BOARD_HEIGHT])
    inner_cutout.apply_translation([
        THICKNESS + CLEARANCE + BOARD_WIDTH / 2,
        THICKNESS + CLEARANCE + BOARD_LENGTH / 2,
        THICKNESS + BOARD_HEIGHT / 2
    ])
    base = base.difference(inner_cutout)

    # Create USB port cutout on the short side
    usb_cutout = trimesh.creation.box(extents=[THICKNESS * 2, USB_PORT_SIZE[1], USB_PORT_SIZE[0]])
    usb_cutout.apply_translation([
        THICKNESS / 2,
        USB_PORT_POSITION[1] + USB_PORT_SIZE[1] / 2,
        USB_PORT_SIZE[0] / 2 + BOARD_HEIGHT / 2
    ])
    base = base.difference(usb_cutout)

    # Create DC jack cutout on the short side
    dc_cutout = trimesh.creation.box(extents=[THICKNESS * 2, DC_JACK_SIZE[1], DC_JACK_SIZE[0]])
    dc_cutout.apply_translation([
        THICKNESS / 2,
        DC_JACK_POSITION[1] + DC_JACK_SIZE[1] / 2,
        DC_JACK_SIZE[0] / 2 + BOARD_HEIGHT / 2
    ])
    base = base.difference(dc_cutout)

    return base

# Generate the top cover of the enclosure using trimesh
def arduino_enclosure_top():
    top_width = BOARD_WIDTH + 2 * CLEARANCE + 2 * THICKNESS
    top_length = BOARD_LENGTH + 2 * CLEARANCE + 2 * THICKNESS
    top_height = THICKNESS * 2

    # Create top box
    top = trimesh.creation.box(extents=[top_width, top_length, top_height])
    top.apply_translation([top_width / 2, top_length / 2, top_height / 2])

    # Create inner cutout
    inner_cutout = trimesh.creation.box(extents=[BOARD_WIDTH, BOARD_LENGTH, THICKNESS])
    inner_cutout.apply_translation([
        THICKNESS + CLEARANCE + BOARD_WIDTH / 2,
        THICKNESS + CLEARANCE + BOARD_LENGTH / 2,
        THICKNESS / 2
    ])
    top = top.difference(inner_cutout)

    # Create header pin cutouts
    # Digital pins header cutout (row 1)
    digital_header_cutout_row_1 = trimesh.creation.box(extents=[52.0, 5.0, top_height])
    digital_header_cutout_row_1.apply_translation([
        THICKNESS + CLEARANCE + 8.0 + digital_header_cutout_row_1.extents[0] / 2,
        THICKNESS + CLEARANCE + BOARD_LENGTH - 5.5,
        top_height / 2
    ])
    top = top.difference(digital_header_cutout_row_1)

    # Analog pins header cutout
    analog_header_cutout = trimesh.creation.box(extents=[52.0, 5.0, top_height])
    analog_header_cutout.apply_translation([
        THICKNESS + CLEARANCE + 8.0 + analog_header_cutout.extents[0] / 2,
        THICKNESS + CLEARANCE + 5.5,
        top_height / 2
    ])
    top = top.difference(analog_header_cutout)

    return top

# Convert enclosure parts to STL files
def convert_to_stl(obj, filename):
    obj.export(filename, file_type='stl')

if __name__ == "__main__":
    base = arduino_enclosure_base()
    top = arduino_enclosure_top()
    convert_to_stl(base, 'arduino_enclosure_base.stl')
    convert_to_stl(top, 'arduino_enclosure_top.stl')
    print("STL files for Arduino Uno enclosure generated as 'arduino_enclosure_base.stl' and 'arduino_enclosure_top.stl'")
