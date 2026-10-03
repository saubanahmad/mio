"""Generate placeholder animated GIF assets for Mio pet states.

This script creates simple placeholder animations in assets/pet/.
It uses only the Python standard library (struct) to write minimal
GIF89a files with transparency and animation.

These placeholders are intentionally simple and obviously temporary.
They exist to prove the animation architecture works.

Usage:
    python scripts/generate_placeholder_assets.py
"""

from __future__ import annotations

import math
import struct
from pathlib import Path

# Output directory.
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "pet"

# Image dimensions.
WIDTH = 128
HEIGHT = 128


def _lzw_compress(pixels: list[int], min_code_size: int) -> bytes:
    """Minimal LZW compression for GIF image data.

    Args:
        pixels: List of color table indices for each pixel.
        min_code_size: Minimum LZW code size (typically the color table bit depth).

    Returns:
        LZW-compressed data as bytes, formatted as GIF sub-blocks.
    """
    clear_code = 1 << min_code_size
    eoi_code = clear_code + 1

    # Build output as a list of variable-width codes.
    codes: list[int] = []
    code_size = min_code_size + 1
    next_code = eoi_code + 1
    max_code = (1 << code_size) - 1

    # Initialize string table with single-character strings.
    table: dict[tuple[int, ...], int] = {}
    for i in range(clear_code):
        table[(i,)] = i

    codes.append(clear_code)

    buffer: tuple[int, ...] = ()
    for pixel in pixels:
        extended = (*buffer, pixel)
        if extended in table:
            buffer = extended
        else:
            codes.append(table[buffer])
            if next_code <= 4095:
                table[extended] = next_code
                next_code += 1
                if next_code > max_code + 1 and code_size < 12:
                    code_size += 1
                    max_code = (1 << code_size) - 1
            else:
                # Table full — emit clear code and reset.
                codes.append(clear_code)
                table = {}
                for i in range(clear_code):
                    table[(i,)] = i
                code_size = min_code_size + 1
                next_code = eoi_code + 1
                max_code = (1 << code_size) - 1
            buffer = (pixel,)

    if buffer:
        codes.append(table[buffer])
    codes.append(eoi_code)

    # Pack variable-width codes into bytes.
    bit_buffer = 0
    bits_in_buffer = 0
    raw_bytes = bytearray()

    # We need to re-track code size during output.
    code_size = min_code_size + 1
    next_code_out = eoi_code + 1
    max_code_out = (1 << code_size) - 1

    for code in codes:
        bit_buffer |= code << bits_in_buffer
        bits_in_buffer += code_size

        while bits_in_buffer >= 8:
            raw_bytes.append(bit_buffer & 0xFF)
            bit_buffer >>= 8
            bits_in_buffer -= 8

        if code == clear_code:
            code_size = min_code_size + 1
            next_code_out = eoi_code + 1
            max_code_out = (1 << code_size) - 1
        else:
            next_code_out += 1
            if next_code_out > max_code_out + 1 and code_size < 12:
                code_size += 1
                max_code_out = (1 << code_size) - 1

    if bits_in_buffer > 0:
        raw_bytes.append(bit_buffer & 0xFF)

    # Format as GIF sub-blocks (max 255 bytes each).
    output = bytearray()
    offset = 0
    while offset < len(raw_bytes):
        chunk = raw_bytes[offset : offset + 255]
        output.append(len(chunk))
        output.extend(chunk)
        offset += 255
    output.append(0)  # Block terminator.

    return bytes(output)


def _make_circle_pixels(
    width: int,
    height: int,
    cx: float,
    cy: float,
    radius: float,
    fill_index: int,
    outline_index: int,
    bg_index: int = 0,
) -> list[int]:
    """Generate pixel indices for a circle with an outline."""
    pixels = []
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            if dist <= radius - 1.5:
                pixels.append(fill_index)
            elif dist <= radius + 0.5:
                pixels.append(outline_index)
            else:
                pixels.append(bg_index)
    return pixels


def _build_animated_gif(
    width: int,
    height: int,
    colors: list[tuple[int, int, int]],
    frames: list[list[int]],
    delay_cs: int = 15,
    transparent_index: int = 0,
) -> bytes:
    """Build a complete animated GIF89a file.

    Args:
        width: Image width in pixels.
        height: Image height in pixels.
        colors: List of (R, G, B) tuples for the color table.
        frames: List of pixel index lists, one per frame.
        delay_cs: Frame delay in centiseconds (1/100th of a second).
        transparent_index: Index of the transparent color.

    Returns:
        Complete GIF file as bytes.
    """
    # Determine color table size (must be power of 2).
    ct_bits = 1
    while (1 << ct_bits) < len(colors):
        ct_bits += 1
    num_colors = 1 << ct_bits

    # Pad color table.
    padded_colors = list(colors)
    while len(padded_colors) < num_colors:
        padded_colors.append((0, 0, 0))

    data = bytearray()

    # Header.
    data.extend(b"GIF89a")

    # Logical Screen Descriptor.
    packed = 0x80 | ((ct_bits - 1) & 0x07)  # GCT flag + size.
    data.extend(struct.pack("<HH", width, height))
    data.extend(struct.pack("BBB", packed, transparent_index, 0))

    # Global Color Table.
    for r, g, b in padded_colors:
        data.extend(struct.pack("BBB", r, g, b))

    # Netscape Application Extension (loop forever).
    data.extend(b"\x21\xFF\x0BNETSCAPE2.0\x03\x01")
    data.extend(struct.pack("<H", 0))  # Loop count 0 = infinite.
    data.append(0x00)  # Block terminator.

    min_code_size = max(ct_bits, 2)  # GIF minimum is 2.

    for frame_pixels in frames:
        # Graphic Control Extension.
        data.extend(b"\x21\xF9\x04")
        # Disposal method 1 (do not dispose), transparent flag.
        data.extend(struct.pack("B", 0x05))  # Dispose: none, transparent: yes.
        data.extend(struct.pack("<H", delay_cs))
        data.extend(struct.pack("B", transparent_index))
        data.append(0x00)  # Block terminator.

        # Image Descriptor.
        data.append(0x2C)
        data.extend(struct.pack("<HH", 0, 0))  # Left, top.
        data.extend(struct.pack("<HH", width, height))
        data.append(0x00)  # No local color table.

        # Image Data.
        data.append(min_code_size)
        data.extend(_lzw_compress(frame_pixels, min_code_size))

    # Trailer.
    data.append(0x3B)

    return bytes(data)


def generate_idle_gif(path: Path) -> None:
    """Generate a simple idle animation: a pulsing blue circle."""
    # Colors: 0=transparent, 1=body, 2=outline, 3=eye, 4=body-pulse
    colors = [
        (0, 0, 0),        # 0: transparent
        (180, 220, 255),   # 1: body (light blue)
        (120, 170, 220),   # 2: outline
        (60, 60, 80),      # 3: eyes/features
        (170, 210, 245),   # 4: body pulse (slightly different)
    ]

    cx, cy = WIDTH / 2, HEIGHT / 2

    frames = []

    # Frame 1: Normal size.
    pixels = _make_circle_pixels(WIDTH, HEIGHT, cx, cy, 42, 1, 2)
    # Add eyes.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = y * WIDTH + x
            # Left eye.
            if math.sqrt((x - cx + 12) ** 2 + (y - cy + 8) ** 2) <= 4:
                pixels[idx] = 3
            # Right eye.
            if math.sqrt((x - cx - 12) ** 2 + (y - cy + 8) ** 2) <= 4:
                pixels[idx] = 3
    frames.append(pixels)

    # Frame 2: Slightly smaller (pulse effect).
    pixels2 = _make_circle_pixels(WIDTH, HEIGHT, cx, cy, 40, 4, 2)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = y * WIDTH + x
            if math.sqrt((x - cx + 12) ** 2 + (y - cy + 8) ** 2) <= 4:
                pixels2[idx] = 3
            if math.sqrt((x - cx - 12) ** 2 + (y - cy + 8) ** 2) <= 4:
                pixels2[idx] = 3
    frames.append(pixels2)

    # Frame 3: Back to normal (smooth loop).
    frames.append(list(frames[0]))

    gif_data = _build_animated_gif(WIDTH, HEIGHT, colors, frames, delay_cs=40)
    path.write_bytes(gif_data)
    print(f"  Created: {path} ({len(gif_data)} bytes, {len(frames)} frames)")


def generate_dragging_gif(path: Path) -> None:
    """Generate a simple dragging animation: a squished orange circle."""
    # Colors: 0=transparent, 1=body, 2=outline, 3=eye, 4=body-variant
    colors = [
        (0, 0, 0),        # 0: transparent
        (255, 200, 150),   # 1: body (warm orange)
        (220, 160, 100),   # 2: outline
        (60, 60, 80),      # 3: eyes/features
        (255, 210, 160),   # 4: body variant
    ]

    cx, cy = WIDTH / 2, HEIGHT / 2

    frames = []

    # Frame 1: Slightly wide (squished horizontally = being grabbed).
    pixels = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Ellipse: wider than tall.
            dx = (x - cx) / 46  # wider
            dy = (y - cy) / 36  # shorter
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= 0.90:
                pixels.append(1)
            elif dist <= 1.0:
                pixels.append(2)
            else:
                pixels.append(0)
    # Add squinted eyes.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = y * WIDTH + x
            # Left eye (squinted — wider, shorter).
            dx_e = abs(x - (cx - 12))
            dy_e = abs(y - (cy - 4))
            if dx_e <= 5 and dy_e <= 2:
                pixels[idx] = 3
            # Right eye.
            dx_e2 = abs(x - (cx + 12))
            if dx_e2 <= 5 and dy_e <= 2:
                pixels[idx] = 3
    frames.append(pixels)

    # Frame 2: Slightly different squish.
    pixels2 = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = (x - cx) / 44
            dy = (y - cy) / 38
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= 0.90:
                pixels2.append(4)
            elif dist <= 1.0:
                pixels2.append(2)
            else:
                pixels2.append(0)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = y * WIDTH + x
            dx_e = abs(x - (cx - 12))
            dy_e = abs(y - (cy - 4))
            if dx_e <= 5 and dy_e <= 2:
                pixels2[idx] = 3
            dx_e2 = abs(x - (cx + 12))
            if dx_e2 <= 5 and dy_e <= 2:
                pixels2[idx] = 3
    frames.append(pixels2)

    gif_data = _build_animated_gif(WIDTH, HEIGHT, colors, frames, delay_cs=20)
    path.write_bytes(gif_data)
    print(f"  Created: {path} ({len(gif_data)} bytes, {len(frames)} frames)")


def main() -> None:
    """Generate all placeholder pet assets."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating placeholder assets in: {ASSETS_DIR}")

    generate_idle_gif(ASSETS_DIR / "idle.gif")
    generate_dragging_gif(ASSETS_DIR / "dragging.gif")

    print("Done.")


if __name__ == "__main__":
    main()
