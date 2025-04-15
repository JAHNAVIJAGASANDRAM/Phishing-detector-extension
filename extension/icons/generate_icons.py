import cairosvg
import os

def generate_icons(source_svg, sizes):
    basename = os.path.splitext(source_svg)[0]
    for size in sizes:
        output_file = f"{basename}{size}.png"
        try:
            with open(source_svg, 'r') as f:
                svg_content = f.read()
            cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                write_to=output_file,
                output_width=size,
                output_height=size
            )
            print(f"Generated {output_file}")
        except Exception as e:
            print(f"Error generating {output_file}: {e}")

# Sizes needed for Chrome extension
sizes = [16, 48, 128]

# Generate warning icons
if os.path.exists('icon_warning.svg'):
    generate_icons('icon_warning.svg', sizes)
    # Rename files to match extension requirements
    for size in sizes:
        os.rename(f'icon_warning{size}.png', f'icon{size}_warning.png')

# Generate safe icons
if os.path.exists('icon_safe.svg'):
    generate_icons('icon_safe.svg', sizes)
    # Rename files to match extension requirements
    for size in sizes:
        os.rename(f'icon_safe{size}.png', f'icon{size}.png')

print("Icon generation complete!") 