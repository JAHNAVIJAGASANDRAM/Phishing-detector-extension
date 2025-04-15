import cairosvg
import os

def convert_svg_to_png(svg_file):
    png_file = svg_file.replace('.svg', '.png')
    try:
        with open(svg_file, 'r') as f:
            svg_content = f.read()
        cairosvg.svg2png(bytestring=svg_content.encode('utf-8'),
                        write_to=png_file)
        print(f"Converted {svg_file} to {png_file}")
    except Exception as e:
        print(f"Error converting {svg_file}: {e}")

# List of SVG files to convert
svg_files = [
    'icon16.svg',
    'icon48.svg',
    'icon128.svg',
    'icon16_warning.svg',
    'icon48_warning.svg',
    'icon128_warning.svg'
]

# Convert each SVG file
for svg_file in svg_files:
    if os.path.exists(svg_file):
        convert_svg_to_png(svg_file)
    else:
        print(f"File not found: {svg_file}") 