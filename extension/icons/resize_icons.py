from PIL import Image
import os

def resize_icon(source_image, output_name, size):
    try:
        img = Image.open(source_image)
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        img.save(output_name)
        print(f"Generated {output_name}")
    except Exception as e:
        print(f"Error generating {output_name}: {e}")

# Sizes needed for Chrome extension
sizes = [16, 48, 128]

# Resize warning icons
if os.path.exists('base_warning.png'):
    for size in sizes:
        resize_icon('base_warning.png', f'icon{size}_warning.png', size)

# Resize safe icons
if os.path.exists('base_safe.png'):
    for size in sizes:
        resize_icon('base_safe.png', f'icon{size}.png', size)

print("Icon generation complete!") 