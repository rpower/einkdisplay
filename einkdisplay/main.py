#! /usr/bin/python3
import os
import socket
import random
from PIL import Image

def get_random_image(images_folder = 'images', previous_images_file = 'images/previous_images.txt', image_freshness = 5):
    """
    Calculates which image should be shown next and tries not to repeat 'recent' images
    :param images_folder: The name of the folder where the images are stored
    :param previous_images_file: A .txt file which will store recent images shown on the display
    :param image_freshness: The minimum number of images to be shown on the display before a repeat is shown
    :return: A path to the next image to be shown on the display
    """
    # image_freshness = number of images before seeing a previous image
    # A value of 5 means that a new image can't be one of the previous 5 images shown
    while True:
        random_file = random.choice(os.listdir(images_folder))

        # Create list of images
        with open(previous_images_file, 'r') as f:
            lines_in_file = f.readlines()
        # Check that proposed image was not already previously shown
        if (random_file + '\n') not in lines_in_file:
            break

    # Write previous images to file
    new_lines_in_file = lines_in_file[1:image_freshness]
    with open(previous_images_file, 'w') as f:
        f.write(''.join(new_lines_in_file))
        f.write(random_file)
        f.write('\n')

        return images_folder + '/' + random_file

def display_image(path_to_image, saturation = 0.7, rotate = None, is_local = False, show_images = True):
    """
    Displays a new image on the einkdisplay
    :param path_to_image: The file path of the image to display
    :param saturation: How saturated the image on the display should be
    :param rotate: Rotation needed on the image before displaying
    :param is_local: Flag whether function is run locally or not (running locally will display the image on-screen as
    opposed to trying to find the einkdisplay device
    :param show_images: Flag whether or not to display images on-screen when being run locally
    :return: Returns nothing
    """
    if not is_local:
        from inky.inky_uc8159 import Inky
        inky = Inky()

    # Get image
    image = Image.open(path_to_image)

    # Rotate image
    if rotate == 'left':
        rotate_degrees = 270
    elif rotate == 'right':
        rotate_degrees = 90
    else:
        rotate_degrees = 0
    image = image.rotate(rotate_degrees, expand=True)

    # Resize image
    if not is_local:
        display_height, display_width = inky.resolution
    else:
        display_width, display_height = (448, 600)
    display_height_to_width_ratio = display_height / display_width
    image_height, image_width = image.size

    ideal_image_height = image_width * display_height_to_width_ratio
    if is_local and show_images:
        image.show()

    if image_height > ideal_image_height:
        box_to_crop = (0, 0, ideal_image_height, image_width)
        image = image.crop(box_to_crop)

    # Rotate image back again for local display
    if is_local:
        image = image.rotate(360 - rotate_degrees, expand=True)

    if is_local and show_images:
        image.show()

    # Final resize
    image = image.resize((display_height, display_width))

    # Display image
    if not is_local:
        final_image_height, final_image_width = image.size
        inky.set_image(image, saturation=saturation)
        inky.show()

def write_text():
    from PIL import Image, ImageFont, ImageDraw
    from font_intuitive import Intuitive
    from inky.auto import auto

    inky = auto(ask_user=True, verbose=True)

    img = Image.new('P', inky.resolution)
    draw = ImageDraw.Draw(img)

    scale_size = 1
    intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))

    # Set background colour to white
    for y in range(inky.height - 1):
        for x in range(inky.width - 1):
            print('x:', x)
            print('y:', y)
            inky.set_pixel(x, y, inky.WHITE)

    # Write text
    draw.text((0, 0), 'Hello', inky.BLACK, font = intuitive_font)

    inky.set_image(img)
    inky.show()

def is_running_locally():
    """
    Uses hostname to determine whether this script is being run on the pi (remotely) or being run locally
    :return: Boolean, True if running locally, False otherwise
    """
    pi_host_name = 'raspberrypizero'
    current_host_name = socket.gethostname()
    return current_host_name != pi_host_name

if __name__ == "__main__":
    display_images_mode = True

    if display_images_mode:
        random_image = get_random_image()

        display_image(
            path_to_image = random_image,
            rotate = 'left',
            is_local = is_running_locally()
        )
    else:
        write_text()