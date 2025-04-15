import os
from PIL import Image, ImageDraw

def create_warning_icon(size):
    """Create a warning icon directly using PIL"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate triangle points
    padding = size // 10
    points = [
        (size // 2, padding),  # top
        (size - padding, size - padding),  # bottom right
        (padding, size - padding)  # bottom left
    ]
    
    # Draw red triangle
    draw.polygon(points, fill='#F44336', outline='white')
    
    # Draw exclamation mark
    mark_width = max(1, size // 8)
    mark_x = (size - mark_width) // 2
    mark_y_top = size // 3
    mark_y_bottom = size * 2 // 3
    
    # Vertical line
    draw.rectangle([mark_x, mark_y_top, mark_x + mark_width, mark_y_bottom], fill='white')
    
    # Dot
    dot_y = mark_y_bottom + mark_width
    draw.ellipse([mark_x, dot_y, mark_x + mark_width, dot_y + mark_width], fill='white')
    
    return img

def create_safe_icon(size):
    """Create a safe icon directly using PIL"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate triangle points
    padding = size // 10
    points = [
        (size // 2, padding),  # top
        (size - padding, size - padding),  # bottom right
        (padding, size - padding)  # bottom left
    ]
    
    # Draw green triangle
    draw.polygon(points, fill='#4CAF50', outline='white')
    
    # Draw checkmark
    check_width = max(1, size // 8)
    center_x = size // 2
    center_y = size * 3 // 5
    
    # Calculate checkmark points
    left = (center_x - size//4, center_y)
    middle = (center_x, center_y + size//4)
    right = (center_x + size//3, center_y - size//4)
    
    # Draw checkmark
    draw.line([left, middle, right], fill='white', width=check_width)
    
    return img

# Create icons in all required sizes
sizes = [16, 48, 128]

try:
    # Create warning icons
    for size in sizes:
        warning_icon = create_warning_icon(size)
        warning_icon.save(f'icon{size}_warning.png')
        print(f'Created icon{size}_warning.png')
        
    # Create safe icons
    for size in sizes:
        safe_icon = create_safe_icon(size)
        safe_icon.save(f'icon{size}.png')
        print(f'Created icon{size}.png')
        
    print("All icons created successfully!")
    
except Exception as e:
    print(f"Error creating icons: {e}") 