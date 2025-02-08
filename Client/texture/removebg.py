from PIL import Image
import os

def remove_background(image_path, output_path):
    # Open the image
    img = Image.open(image_path).convert("RGBA")
    
    # Get pixel data
    data = img.load()

    # Get the background color (top-left pixel)
    bg_color = data[0, 0]

    # Create a new image for the output
    new_data = []

    for y in range(img.height):
        for x in range(img.width):
            current_color = data[x, y]
            # Compare current pixel to the background color
            if current_color[:3] == bg_color[:3]:  # Ignore alpha channel
                new_data.append((0, 0, 0, 0))  # Transparent
            else:
                new_data.append(current_color)

    # Update the image data
    img.putdata(new_data)
    
    # Save the result
    img.save(output_path, "PNG")
    print(f"Processed image saved at {output_path}")

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")
            remove_background(input_path, output_path)

# Example usage
input_directory = "NoRemoveBgCards"  # Replace with your input directory
output_directory = "cards"  # Replace with your output directory
process_directory(input_directory, output_directory)
