import zlib
import struct
import math
import random
import os

def write_png(filename, width, height, pixels):
    """
    Writes RGB pixels (list of (R, G, B) tuples of length width*height) as a valid PNG.
    """
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # Filter byte 0 (None)
        row_start = y * width
        for x in range(width):
            r, g, b = pixels[row_start + x]
            raw_data.append(int(max(0, min(255, r))))
            raw_data.append(int(max(0, min(255, g))))
            raw_data.append(int(max(0, min(255, b))))

    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

    magic = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(bytes(raw_data), 9))
    iend = chunk(b"IEND", b"")

    with open(filename, "wb") as f:
        f.write(magic + ihdr + idat + iend)

def create_lesion(width=224, height=224, lesion_type='melanoma'):
    pixels = []
    cx, cy = width / 2.0, height / 2.0

    for y in range(height):
        for x in range(width):
            # Distance from center with organic perturbation
            dx = (x - cx) / (width * 0.38)
            dy = (y - cy) / (height * 0.38)
            dist = math.sqrt(dx * dx + dy * dy)

            # Skin base tone (Fitzpatrick II/III)
            skin_r = 235 + random.uniform(-4, 4)
            skin_g = 195 + random.uniform(-4, 4)
            skin_b = 175 + random.uniform(-4, 4)

            # Subtle vignette
            edge_factor = math.sqrt(((x - cx)**2 + (y - cy)**2)) / (width * 0.7)
            skin_r = max(0, skin_r - edge_factor * 30)
            skin_g = max(0, skin_g - edge_factor * 35)
            skin_b = max(0, skin_b - edge_factor * 35)

            if lesion_type == 'melanoma':
                # Asymmetric pigmented network
                angle = math.atan2(dy, dx)
                perturb = 0.22 * math.sin(3 * angle) + 0.12 * math.cos(5 * angle)
                effective_dist = dist + perturb

                if effective_dist < 0.85:
                    core = 1.0 - (effective_dist / 0.85)
                    # Pigments: dark brown, black, reddish blue
                    r = int(skin_r * (1 - core) + (45 + random.uniform(-10, 15)) * core)
                    g = int(skin_g * (1 - core) + (30 + random.uniform(-10, 10)) * core)
                    b = int(skin_b * (1 - core) + (25 + random.uniform(-10, 10)) * core)
                elif effective_dist < 1.05:
                    edge = (1.05 - effective_dist) / 0.2
                    r = int(skin_r * (1 - edge) + 120 * edge)
                    g = int(skin_g * (1 - edge) + 70 * edge)
                    b = int(skin_b * (1 - edge) + 55 * edge)
                else:
                    r, g, b = int(skin_r), int(skin_g), int(skin_b)

            elif lesion_type == 'psoriasis':
                # Well-demarcated salmon pink erythematous plaque with silvery scale
                angle = math.atan2(dy, dx)
                perturb = 0.15 * math.sin(4 * angle)
                effective_dist = dist + perturb

                if effective_dist < 0.75:
                    core = 1.0 - (effective_dist / 0.75)
                    # Salmon pink plaque
                    base_pr = 205 + random.uniform(-10, 10)
                    base_pg = 90 + random.uniform(-8, 8)
                    base_pb = 100 + random.uniform(-8, 8)
                    # Silvery micaceous scale
                    if random.random() < 0.35 and core > 0.3:
                        scale = random.uniform(0.6, 0.9)
                        r = int(base_pr * (1 - scale) + 240 * scale)
                        g = int(base_pg * (1 - scale) + 235 * scale)
                        b = int(base_pb * (1 - scale) + 235 * scale)
                    else:
                        r, g, b = int(base_pr), int(base_pg), int(base_pb)
                elif effective_dist < 0.95:
                    edge = (0.95 - effective_dist) / 0.2
                    r = int(skin_r * (1 - edge) + 215 * edge)
                    g = int(skin_g * (1 - edge) + 130 * edge)
                    b = int(skin_b * (1 - edge) + 135 * edge)
                else:
                    r, g, b = int(skin_r), int(skin_g), int(skin_b)

            else: # eczema
                # Ill-defined erythematous rash with microvesiculation
                noise = random.uniform(-0.25, 0.25)
                effective_dist = dist + noise
                if effective_dist < 0.9:
                    strength = 1.0 - (effective_dist / 0.9)
                    r = int(skin_r * (1 - strength * 0.7) + (220 + random.uniform(-10, 10)) * (strength * 0.7))
                    g = int(skin_g * (1 - strength * 0.7) + (110 + random.uniform(-10, 10)) * (strength * 0.7))
                    b = int(skin_b * (1 - strength * 0.7) + (115 + random.uniform(-10, 10)) * (strength * 0.7))
                else:
                    r, g, b = int(skin_r), int(skin_g), int(skin_b)

            pixels.append((r, g, b))

    return pixels

def jet_colormap(val):
    """Maps val [0, 1] to Jet RGB colormap."""
    val = max(0.0, min(1.0, val))
    if val < 0.125:
        r, g, b = 0, 0, int(128 + 127 * (val / 0.125))
    elif val < 0.375:
        f = (val - 0.125) / 0.25
        r, g, b = 0, int(255 * f), 255
    elif val < 0.625:
        f = (val - 0.375) / 0.25
        r, g, b = int(255 * f), 255, int(255 * (1 - f))
    elif val < 0.875:
        f = (val - 0.625) / 0.25
        r, g, b = 255, int(255 * (1 - f)), 0
    else:
        f = (val - 0.875) / 0.125
        r, g, b = int(255 * (1 - 0.5 * f)), 0, 0
    return r, g, b

def create_heatmap_and_overlay(orig_pixels, width=224, height=224):
    heat_pixels = []
    overlay_pixels = []
    cx, cy = width / 2.0, height / 2.0

    for y in range(height):
        for x in range(width):
            dx = (x - cx) / (width * 0.28)
            dy = (y - cy) / (height * 0.28)
            d2 = dx * dx + dy * dy
            intensity = math.exp(-0.5 * d2) # Gaussian peak at center lesion
            intensity = max(0.0, min(1.0, intensity * 1.15))

            hr, hg, hb = jet_colormap(intensity)
            heat_pixels.append((hr, hg, hb))

            # Blend 60% heatmap + 40% original
            idx = y * width + x
            or_val, og_val, ob_val = orig_pixels[idx]
            ov_r = int(or_val * 0.45 + hr * 0.55)
            ov_g = int(og_val * 0.45 + hg * 0.55)
            ov_b = int(ob_val * 0.45 + hb * 0.55)
            overlay_pixels.append((ov_r, ov_g, ov_b))

    return heat_pixels, overlay_pixels

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print("Generating sample benchmark images...")
    mel_pixels = create_lesion(224, 224, 'melanoma')
    write_png(os.path.join(out_dir, 'sample_melanoma.png'), 224, 224, mel_pixels)

    pso_pixels = create_lesion(224, 224, 'psoriasis')
    write_png(os.path.join(out_dir, 'sample_psoriasis.png'), 224, 224, pso_pixels)

    ecz_pixels = create_lesion(224, 224, 'eczema')
    write_png(os.path.join(out_dir, 'sample_eczema.png'), 224, 224, ecz_pixels)

    heat_pixels, over_pixels = create_heatmap_and_overlay(mel_pixels, 224, 224)
    write_png(os.path.join(out_dir, 'sample_heatmap.png'), 224, 224, heat_pixels)
    write_png(os.path.join(out_dir, 'sample_overlay.png'), 224, 224, over_pixels)

    print("Sample benchmark assets generated successfully.")
