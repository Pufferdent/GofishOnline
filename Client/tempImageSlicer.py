from PIL import Image
import os

from PIL import Image
import os

def slice_image(image_path, output_dir, start_x, start_y, block_width, block_height):
    # Open the image
    image = Image.open(image_path)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get image dimensions
    img_width, img_height = image.size

    # Loop through the image and slice it into blocks
    block_count = 0
    y = start_y
    while y < img_height:
        x = start_x
        while x < img_width:
            # Calculate the block's boundaries using rounding for float dimensions
            left = int(round(x))
            upper = int(round(y))
            right = int(round(min(x + block_width, img_width)))
            lower = int(round(min(y + block_height, img_height)))

            # Crop the block
            block = image.crop((left, upper, right, lower))

            # Save the block
            block_filename = f"block_{block_count}.png"
            block.save(os.path.join(output_dir, block_filename))
            block_count += 1

            x += block_width
        y += block_height

    print(f"Sliced {block_count} blocks and saved to {output_dir}")

# Parameters
image_path = "texture/raw_card_2.jpg"  # Replace with your image path
output_dir = "texture/cards/"           # Directory to save the slices
start_x = 30                            # Starting x-coordinate
start_y = 30                            # Starting y-coordinate
block_width = 72.5                        # Block width
block_height = 100                      # Block height

slice_image(image_path, output_dir, start_x, start_y, block_width, block_height)
