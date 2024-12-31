import os
from PIL import Image

# Base path for storing files
BASE_PATH = 'user_planets'
if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

def embed_message(image, message, unique_id):
    """Embed a message into an image and save with a unique filename."""
    # Ensure the image is in RGBA mode to maintain transparency
    img = image.convert("RGBA")
    pixels = img.load()

    width, height = img.size
    x, y = width // 2, height // 2  # Start in the center of the image
    dx, dy = 0, -1  # Initial direction (up)

    # Encode the message with a custom end pattern
    end_pattern = b'\x01\x02\x03'
    message_bytes = message.encode() + end_pattern
    message_length = len(message_bytes) * 8  # Total number of bits to embed

    if message_length > (width * height):  # Ensure the image is large enough
        raise ValueError("Image is too small to store the message")

    for bit in range(message_length):
        if (x >= width) or (y >= height) or (x < 0) or (y < 0):
            break  # Stop if out of bounds

        r, g, b, a = pixels[x, y]

        # Embed each bit in the red channel's least significant bit
        if (message_bytes[bit // 8] >> (7 - (bit % 8))) & 1:
            r = (r & ~1) | 1  # Set the LSB to 1
        else:
            r = (r & ~1)  # Set the LSB to 0

        # Update the pixel
        pixels[x, y] = (r, g, b, a)  # Ensure alpha is preserved

        # Change direction if needed for spiral pattern
        if (x == y) or (x + y == width - 1):
            dx, dy = -dy, dx  # Change direction

        x += dx
        y += dy

    # Generate unique filename and save the modified image
    unique_filename = f"blessID_{unique_id}.png"
    save_path = os.path.join(BASE_PATH, unique_filename)
    img.save(save_path)

    print("Message embedded in magic order.")
    return save_path  # Return path to the saved encrypted image

def extract_message(image_path):
    """Extract the embedded message from an image."""
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()

    width, height = img.size
    x, y = width // 2, height // 2  # Start in the center of the image
    dx, dy = 0, -1  # Initial direction (up)

    bits = []

    while True:
        if (x >= width) or (y >= height) or (x < 0) or (y < 0):
            break  # Stop if out of bounds

        r, g, b, a = pixels[x, y]

        # Extract the least significant bit from the red channel
        bit = r & 0x01
        bits.append(bit)

        # Change direction if needed for spiral pattern
        if (x == y) or (x + y == width - 1):
            dx, dy = -dy, dx  # Change direction

        x += dx
        y += dy

    # Convert bits back to bytes
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte |= (bits[i + j] << (7 - j))
        byte_array.append(byte)

    # Look for the custom end pattern
    end_pattern = b'\x01\x02\x03'
    if end_pattern in byte_array:
        byte_array = byte_array[:byte_array.index(end_pattern)]  # Trim to the end pattern

    return byte_array.decode('utf-8', errors='ignore')

# Example usage of embedding and extracting a message
if __name__ == "__main__":
    user_id = 123456789  # Example user ID
    original_message = "this is halloween"
    
    # Example image (you can replace this with an actual image path)
    image_path = "path/to/your/input_image.png"

    # Open image and embed message
    image = Image.open(image_path)
    encrypted_image_path = embed_message(image, original_message, user_id)
    print(f"Encrypted image saved at: {encrypted_image_path}")

    # Extract message from the saved encrypted image
    extracted_message = extract_message(encrypted_image_path)
    print("Extracted message:", extracted_message)