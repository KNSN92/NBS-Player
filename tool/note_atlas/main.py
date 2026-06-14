
from itertools import product, permutations
import json
from os import mkdir
import numpy as np
from PIL import Image, ImageFilter
import random as rand

def iter_rect(x, y, w, h):
    for (x, y) in product(range(x, x + w), range(y, y + h)):
        yield (x, y)

def soft_light(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return np.where(blend >= 0.5, 2.0 * base * blend + base * base * (1.0 - 2.0 * blend), np.sqrt(base) * (2.0 * blend - 1.0) + (2.0 * base) * (1.0 - blend))

def lighten(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return np.maximum(base, blend)

def darken(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return np.minimum(base, blend)

def hard_light(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return np.where(blend <= 0.5, 2.0 * base * blend, 1.0 - 2.0 * (1.0 - base) * (1.0 - blend))

def multiply(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return base * blend

def color_burn(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return np.where(blend == 0.0, 0.0, 1.0 - np.minimum(1.0, 1.0 - base) / blend)

def color_screen(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return 1.0 - (1.0 - base) * (1.0 - blend)

def overlay(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    return np.where(base <= 0.5, 2.0 * base * blend, 1.0 - 2.0 * (1.0 - base) * (1.0 - blend))

# Minecraft Dye Colors
# COLORS = [
#     (0xF9, 0xFF, 0xFE), # white
#     (0xF9, 0x80, 0x1D), # orange
#     (0xC7, 0x4E, 0xBD), # magenta
#     (0x3A, 0xB3, 0xDA), # light blue
#     (0xFE, 0xD8, 0x3D), # yellow
#     (0x80, 0xC7, 0x1F), # lime
#     (0xF3, 0x8B, 0xAA), # pink
#     (0x47, 0x4F, 0x52), # gray
#     (0x9D, 0x9D, 0x97), # light gray
#     (0x16, 0x9C, 0x9C), # cyan
#     (0x89, 0x32, 0xB8), # purple
#     (0x3C, 0x44, 0xAA), # blue
#     (0x83, 0x54, 0x32), # brown
#     (0x5E, 0x7C, 0x16), # green
#     (0xB0, 0x2E, 0x26), # red
#     (0x1D, 0x1D, 0x21), # black
# ]

# Minecraft Note Block Studio Note Colors
COLORS = [
    (0x19, 0x64, 0xac),
    (0x3c, 0x8e, 0x48),
    (0xbe, 0x6b, 0x6b),
    (0xbe, 0xbe, 0x19),
    (0x9d, 0x5a, 0x98),
    (0x57, 0x2b, 0x21),
    (0xbe, 0xc6, 0x5c),
    (0xbe, 0x19, 0xbe),
    (0x52, 0x90, 0x8d),
    (0xbe, 0xbe, 0xbe),
    (0x19, 0x91, 0xbe),
    (0xbe, 0x23, 0x28),
    (0xbe, 0x57, 0x28),
    (0x19, 0xbe, 0x19),
    (0xbe, 0x19, 0x57),
    (0x57, 0x57, 0x57),
]

try:
    mkdir("note_atlas")
except FileExistsError:
    pass
atlas_img_file = "atlas.png"
atlas_json_file = "atlas.json"
# Best seed, i think. If you don't like this sequence, change this value to your favorite one.
seed = 157

def blend(base, blend):
    colored_note_img = overlay(base, blend)
    # decrease contrast
    colored_note_img[:, :, 0] = (colored_note_img[:, :, 0] + np.average(colored_note_img[:, :, 0])) / 2
    colored_note_img[:, :, 1] = (colored_note_img[:, :, 1] + np.average(colored_note_img[:, :, 1])) / 2
    colored_note_img[:, :, 2] = (colored_note_img[:, :, 2] + np.average(colored_note_img[:, :, 2])) / 2
    return colored_note_img

note_img = np.array(Image.open("noteblock.png").convert("RGB")) / 255.0
(note_width, note_height) = note_img.shape[:2]

atlas_img = Image.new("RGB", (note_width * len(COLORS), note_height * len(COLORS)))
atlas_frame_data = [("", (0, 0))] * (len(COLORS) ** 2)

for i, color in enumerate(COLORS):
    colored_note_img = np.zeros((note_height, note_width, 3))
    colored_note_img[:, :, 0] = color[0] / 255.0
    colored_note_img[:, :, 1] = color[1] / 255.0
    colored_note_img[:, :, 2] = color[2] / 255.0
    colored_note_img = blend(note_img, colored_note_img)
    colored_note_img = (colored_note_img * 255).astype(np.uint8)
    colored_note_img = Image.fromarray(colored_note_img)
    atlas_img.paste(colored_note_img, (i * note_width, 0 * note_height))
    atlas_frame_data[i] = (f"note_{i}", (i * note_width, 0))

color_pairs = list(permutations(COLORS, 2))
rand.seed(seed)
rand.shuffle(color_pairs)

for i, (color1, color2) in enumerate(color_pairs):
    x = i % len(COLORS)
    y = i // len(COLORS) + 1
    colored_note_img = np.zeros((note_height, note_width, 3))
    colored_note_img[:, :, 0] = np.linspace(color1[0] / 255.0, color2[0] / 255.0, note_height)[:, None]
    colored_note_img[:, :, 1] = np.linspace(color1[1] / 255.0, color2[1] / 255.0, note_height)[:, None]
    colored_note_img[:, :, 2] = np.linspace(color1[2] / 255.0, color2[2] / 255.0, note_height)[:, None]
    colored_note_img = blend(note_img, colored_note_img)
    colored_note_img = (colored_note_img * 255).astype(np.uint8)
    colored_note_img = Image.fromarray(colored_note_img)
    atlas_img.paste(colored_note_img, (x * note_width, y * note_height))
    atlas_frame_data[y * len(COLORS) + x] = (f"note_{y * len(COLORS) + x}", (x * note_width, y * note_height))

atlas_img.save(f"note_atlas/{atlas_img_file}")

atlas_frames = {}
for name, (x, y) in atlas_frame_data:
    atlas_frames[f"{name}.png"] = {
        "frame": {"x": x, "y": y, "w": note_width, "h": note_height},
        "rotated": False,
        "trimmed": False,
        "spriteSourceSize": {"x": 0, "y": 0, "w": note_width, "h": note_height},
        "sourceSize": {"w": note_width, "h": note_height}
    }

atlas_data = {
    "frames": atlas_frames,
    "meta": {
        "image": atlas_img_file,
        "format": "RGB888",
        "size": {"w": atlas_img.width, "h": atlas_img.height},
        "scale": "1"
    }
}

with open(f"note_atlas/{atlas_json_file}", "w") as f:
    json.dump(atlas_data, f, indent=4)
