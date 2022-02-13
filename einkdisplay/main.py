#! /usr/bin/python3
import os
import random
from PIL import Image

display_images_mode = True

def get_random_image(images_folder = 'images', previous_images_file = 'images/previous_images.txt', image_freshness = 5):
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
    print('Image:', path_to_image)
    print('display_width:', display_width)
    print('display_height:', display_height)
    print('image_width:', image_width)
    print('image_height:', image_height)

    ideal_image_height = image_width * display_height_to_width_ratio
    print('ideal_image_height:', ideal_image_height)
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
        print('final_image_width:', final_image_width)
        print('final_image_height:', final_image_height)
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

if display_images_mode:
    random_image = get_random_image()

    display_image(
        path_to_image = random_image,
        rotate = 'left',
        is_local = False
    )
else:
    write_text()