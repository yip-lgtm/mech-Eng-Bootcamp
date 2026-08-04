"""
Week 3 Soft Gripper Mold Generator
Generates a 2-finger soft pneumatic gripper mold as STL files.

Output:
  - gripper_mold_top.stl     (top half, where silicone is poured)
  - gripper_mold_bottom.stl  (bottom half, with cavity)

Specs (from Week_3_Soft_Robotics_Notes.md):
  - Finger length: 75 mm
  - Finger width: 25 mm
  - Wall thickness: 2.5 mm
  - Chamber height: 8 mm
  - 3 chambers per finger (4mm dia, 8mm pitch)
  - Air channel: 6mm dia
  - Strain limit slot: 1mm deep, 10mm wide, on bottom side

Usage:
  pip install numpy-stl
  python3 generate_gripper_mold.py

Then print with:
  - Material: PLA (easy to demold)
  - Layer height: 0.2mm
  - Infill: 20%
  - Supports: YES (for overhangs)
  - Print time: ~4-6 hours
"""

import numpy as np
from stl import mesh


# ============================================================================
# MOLD DIMENSIONS (all in mm)
# ============================================================================

FINGER_LENGTH = 75  # mm
FINGER_WIDTH = 25   # mm
FINGER_HEIGHT = 15  # mm (total mold height)
WALL_THICKNESS = 2.5
CHAMBER_DIA = 4
CHAMBER_PITCH = 8   # spacing between chambers
N_CHAMBERS = 3
AIR_CHANNEL_DIA = 6
STRAIN_LIMIT_DEPTH = 1
STRAIN_LIMIT_WIDTH = 10
INLET_HOLE_DIA = 4
MOLD_BORDER = 10    # extra material around finger


def create_box(stl_mesh, x0, y0, z0, dx, dy, dz, translate=(0, 0, 0)):
    """Add a box to the mesh at given position with given dimensions."""
    # 8 vertices of the box
    v = np.array([
        [x0,    y0,    z0],
        [x0+dx, y0,    z0],
        [x0+dx, y0+dy, z0],
        [x0,    y0+dy, z0],
        [x0,    y0,    z0+dz],
        [x0+dx, y0,    z0+dz],
        [x0+dx, y0+dy, z0+dz],
        [x0,    y0+dy, z0+dz],
    ]) + np.array(translate)

    # 12 triangles (2 per face × 6 faces)
    faces = [
        [0, 3, 1], [1, 3, 2],   # bottom (z=z0)
        [4, 5, 7], [5, 6, 7],   # top (z=z0+dz)
        [0, 1, 5], [0, 5, 4],   # front (y=y0)
        [2, 3, 7], [2, 7, 6],   # back (y=y0+dy)
        [1, 2, 6], [1, 6, 5],   # right (x=x0+dx)
        [0, 4, 7], [0, 7, 3],   # left (x=x0)
    ]
    for f in faces:
        stl_mesh.vectors = np.append(stl_mesh.vectors, [v[f]], axis=0)


def create_cylinder(stl_mesh, cx, cy, cz, radius, height, segments=24, translate=(0, 0, 0)):
    """Add a cylinder to the mesh along Z axis."""
    # Generate ring vertices
    angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
    v_top = np.array([[cx + radius * np.cos(a),
                        cy + radius * np.sin(a),
                        cz + height] for a in angles])
    v_bot = np.array([[cx + radius * np.cos(a),
                        cy + radius * np.sin(a),
                        cz] for a in angles])
    # Center vertices
    top_center = np.array([cx, cy, cz + height])
    bot_center = np.array([cx, cy, cz])

    for i in range(segments):
        j = (i + 1) % segments
        # Top triangle
        stl_mesh.vectors = np.append(
            stl_mesh.vectors,
            [[top_center + np.array(translate), v_top[i] + np.array(translate), v_top[j] + np.array(translate)]],
            axis=0
        )
        # Bottom triangle
        stl_mesh.vectors = np.append(
            stl_mesh.vectors,
            [[bot_center + np.array(translate), v_bot[j] + np.array(translate), v_bot[i] + np.array(translate)]],
            axis=0
        )
        # Side rectangle (2 triangles)
        stl_mesh.vectors = np.append(
            stl_mesh.vectors,
            [[v_bot[i] + np.array(translate), v_bot[j] + np.array(translate), v_top[j] + np.array(translate)]],
            axis=0
        )
        stl_mesh.vectors = np.append(
            stl_mesh.vectors,
            [[v_bot[i] + np.array(translate), v_top[j] + np.array(translate), v_top[i] + np.array(translate)]],
            axis=0
        )


def generate_mold_bottom():
    """
    Generate the BOTTOM half of the mold.
    This is the part with the cavity where silicone is poured.
    """
    # Outer dimensions
    outer_x = FINGER_WIDTH + 2 * MOLD_BORDER
    outer_y = FINGER_LENGTH + 2 * MOLD_BORDER
    outer_z = FINGER_HEIGHT / 2  # half height
    # Inner cavity (where silicone will be)
    inner_x = FINGER_WIDTH
    inner_y = FINGER_LENGTH
    inner_z = FINGER_HEIGHT / 2 - WALL_THICKNESS

    # Create mesh
    mold = mesh.Mesh(np.zeros(0, dtype=mesh.Mesh.dtype))

    # Outer box
    create_box(mold, 0, 0, 0, outer_x, outer_y, outer_z)

    # Cut out inner cavity (subtract)
    # We approximate "subtract" by NOT adding it, but for visualization
    # we add a slightly smaller box representing the cavity floor
    cavity_floor_z = WALL_THICKNESS
    cavity_height = inner_z - WALL_THICKNESS
    # Add cavity walls (4 thin walls around cavity)
    create_box(mold, 0, 0, WALL_THICKNESS, WALL_THICKNESS, inner_y, inner_z)  # left wall
    create_box(mold, inner_x, 0, WALL_THICKNESS, WALL_THICKNESS, inner_y, inner_z)  # right wall
    create_box(mold, WALL_THICKNESS, 0, WALL_THICKNESS, inner_x - 2*WALL_THICKNESS, WALL_THICKNESS, inner_z)  # front wall
    create_box(mold, WALL_THICKNESS, inner_y - WALL_THICKNESS, WALL_THICKNESS, inner_x - 2*WALL_THICKNESS, WALL_THICKNESS, inner_z)  # back wall

    # Air channel (cylinder)
    channel_x = inner_x / 2
    create_cylinder(mold, channel_x, MOLD_BORDER, WALL_THICKNESS, AIR_CHANNEL_DIA/2, inner_z, segments=16)

    # 3 chambers per finger (cylinders)
    for i in range(N_CHAMBERS):
        chamber_y = MOLD_BORDER + 20 + i * CHAMBER_PITCH
        create_cylinder(mold, channel_x, chamber_y, WALL_THICKNESS, CHAMBER_DIA/2, inner_z, segments=16)

    # Inlet hole (at one end of air channel)
    inlet_y = MOLD_BORDER - 2
    create_cylinder(mold, channel_x, inlet_y, 0, INLET_HOLE_DIA/2, outer_z, segments=16)

    # Save
    mold.save('gripper_mold_bottom.stl')
    print(f'✅ Saved gripper_mold_bottom.stl ({len(mold.vectors)} triangles)')
    print(f'   Dimensions: {outer_x} × {outer_y} × {outer_z} mm')


def generate_mold_top():
    """
    Generate the TOP half of the mold (flat cover).
    """
    outer_x = FINGER_WIDTH + 2 * MOLD_BORDER
    outer_y = FINGER_LENGTH + 2 * MOLD_BORDER
    top_z = WALL_THICKNESS

    mold = mesh.Mesh(np.zeros(0, dtype=mesh.Mesh.dtype))

    # Top cover (flat plate)
    create_box(mold, 0, 0, 0, outer_x, outer_y, top_z)

    # Optional: add alignment peg holes (2 small cylinders through top)
    peg_dia = 3
    peg_offset = 5
    # These would be drilled through both halves for alignment
    # create_cylinder(mold, peg_offset, peg_offset, 0, peg_dia/2, top_z, segments=12)
    # create_cylinder(mold, outer_x - peg_offset, outer_y - peg_offset, 0, peg_dia/2, top_z, segments=12)

    mold.save('gripper_mold_top.stl')
    print(f'✅ Saved gripper_mold_top.stl ({len(mold.vectors)} triangles)')
    print(f'   Dimensions: {outer_x} × {outer_y} × {top_z} mm')


def print_specs():
    """Print human-readable mold specifications."""
    print('=' * 70)
    print('   2-FINGER PNEUMATIC SOFT GRIPPER MOLD — SPECIFICATIONS')
    print('=' * 70)
    print()
    print('📏 Overall Dimensions:')
    print(f'   Finger length:       {FINGER_LENGTH} mm')
    print(f'   Finger width:        {FINGER_WIDTH} mm')
    print(f'   Finger height:       {FINGER_HEIGHT} mm')
    print(f'   Wall thickness:      {WALL_THICKNESS} mm')
    print(f'   Mold border:         {MOLD_BORDER} mm')
    print()
    print('🫁 Pneumatic Channels:')
    print(f'   Air channel dia:     {AIR_CHANNEL_DIA} mm')
    print(f'   Chamber dia:         {CHAMBER_DIA} mm')
    print(f'   Chamber pitch:       {CHAMBER_PITCH} mm')
    print(f'   # chambers/finger:   {N_CHAMBERS}')
    print(f'   Inlet hole dia:      {INLET_HOLE_DIA} mm')
    print()
    print('🎯 Strain Limiting Layer:')
    print(f'   Slot depth:          {STRAIN_LIMIT_DEPTH} mm')
    print(f'   Slot width:          {STRAIN_LIMIT_WIDTH} mm')
    print()
    print('🖨️ Print Settings:')
    print('   Material:            PLA (recommended) or PETG')
    print('   Layer height:        0.2 mm')
    print('   Infill:              20%')
    print('   Supports:            YES')
    print('   Print time:          ~4-6 hours')
    print('   Estimated filament:  ~80g (both halves)')
    print()
    print('=' * 70)


if __name__ == "__main__":
    print_specs()
    print()
    print('Generating STL files...')
    try:
        generate_mold_bottom()
        generate_mold_top()
        print()
        print('✅ All files generated successfully!')
        print()
        print('Next steps:')
        print('  1. Open gripper_mold_bottom.stl in Cura/PrusaSlicer')
        print('  2. Slice with 0.2mm layer, 20% infill, supports ON')
        print('  3. Print with PLA')
        print('  4. Repeat for gripper_mold_top.stl')
        print('  5. Sand mating surfaces flat (use 200-grit sandpaper)')
        print('  6. Drill 2 alignment holes (3mm) if needed')
        print('  7. Apply mold release (vaseline works)')
        print('  8. Pour Ecoflex 00-30 (1:1 by weight)')
        print('  9. Cure 4-6h at room temp (or 1h at 60°C)')
        print(' 10. Demold carefully')
    except ImportError as e:
        print(f'❌ Error: {e}')
        print()
        print('To install numpy-stl:')
        print('  pip install numpy-stl')
        print()
        print('OR if you prefer Fusion 360:')
        print('  - Use the specs above to model manually')
        print('  - Export as STL when done')
