from PIL import Image, ImageDraw, ImageFont

GODRICK_IMAGE = "godrick_base.png"
GODRICK = "I command thee, kneel! I am the lord of all that is golden!"

def decode_image(path_to_png):
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    for x in range(x_size):
        for y in range(y_size):
            pixel_value = red_channel.getpixel((x, y))
            # Extract the least significant bit (LSB) of the red channel:
            lsb = pixel_value & 1
            # Set the corresponding pixel in the decoded image with the LSB:
            pixels[x, y] = (lsb * 255, lsb * 255, lsb * 255)

    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save("decoded_image.png")


def write_text(text_to_write, image_for_size):
    # Define the image size and font size
    image = Image.open(image_for_size)
    image_size = image.size
    font_size = 15

    # Create a new image with white background
    text_image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(text_image)

    # Define text color and position
    text_color = (237, 230, 211)
    text_position = (10, 10)

    # Draw the text on the image
    draw.text(text_position, text_to_write, fill=text_color)

    return text_image

def encode_image(image_path, text_image):
    base_image = Image.open(image_path)
    x_size, y_size = base_image.size
    encoded_image = Image.new("RGB", (x_size, y_size))
    base_pixels = base_image.load()
    encoded_pixels = encoded_image.load()
    text_pixels = text_image.load()

    for x in range(x_size):
        for y in range(y_size):
            if x < text_image.width and y < text_image.height:
                r, g, b = base_pixels[x, y]
                text_r, _, _ = text_pixels[x, y]
                r = (r & ~1) | (text_r // 255)
                encoded_pixels[x, y] = (r, g, b)
            else:
                encoded_pixels[x, y] = base_pixels[x, y]

    encoded_image.save("encoded_image.png")


# This is where we run the functions

# TODO: This encodes an image with text, all of the input is already handled for you
text_image = write_text(GODRICK, GODRICK_IMAGE)
encode_image(GODRICK_IMAGE, text_image)

#TODO: This decodes the encoded image:
decode_image("encoded_image.png")

#TODO: This is just to decode the example image
# decode_image("Encoded-Sample.png")
