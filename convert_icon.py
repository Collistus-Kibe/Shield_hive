# Convert PNG to ICO for Windows EXE icon
from PIL import Image
import os

# Load the source image
img = Image.open('shield_hive_icon.png')

# Convert to RGBA if needed
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Create multiple icon sizes for Windows
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icons = []

for size in sizes:
    resized = img.resize(size, Image.Resampling.LANCZOS)
    icons.append(resized)

# Save as ICO with multiple sizes
icons[0].save(
    'shield_hive.ico',
    format='ICO',
    sizes=[(s.width, s.height) for s in icons],
    append_images=icons[1:]
)

print("✅ Created shield_hive.ico successfully!")
