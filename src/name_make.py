import re
import arabic_reshaper
from PIL import Image, ImageDraw, ImageFont

# Convert gross text to plain text
def text_plain(input):
    text = str(input)
    catch = re.findall("[a-zA-Z\u0600-\u06FF\s\d]+", text)

    return ' '.join(catch)


def persian_checker(input):
    text = str(input)
    search = re.search('^[\u0600-\u06FF\s\d]+$', text)

    if search != None:
        return True

# Check the text language
def lang_check(input):
    text = str(input)
    if re.search('[\.\/]', text) == None:
        if persian_checker(input):
            return True

        elif re.search('[a-zA-Z\s\d]+', text) != None:
            return True

        else:
            return False

    else:
        return False

# Create a text image
def name_make(input):
    # Convert input to string
    text = str(input)
    name = text

    img = Image.new('RGBA', (1200, 700), (0, 0, 0, 0))
    img.save('assets/img/image.png'.format(text))

    font_size = 1
    font_file = 'assets/font/unicode.compacta.ttf'
    font = ImageFont.truetype(font_file)

    if persian_checker(text):
        text = arabic_reshaper.reshape(text)
        font_file = 'assets/font/Dana.ttf'

    while font.getsize(text.upper())[0] < img.size[0]:
        font_size += 1
        font = ImageFont.truetype(font_file, font_size)

    font_size -= 1
    font = ImageFont.truetype(font_file, font_size)

    text_height = int(font.getsize(text.upper())[1] / 2)
    half_height = 350 - text_height

    draw = ImageDraw.Draw(img)
    draw.text((0, half_height), text.upper(), font=font, fill=(255, 255, 255))

    img.save(f'assets/img/image.png')

    return str(f'assets/img/image.png')


# Make the final image
def poster(input):
    text = str(input).lower()

    img = Image.new('RGB', (1200, 700), (0, 0, 0))
    img.save('assets/img/image.png'.format(text))

    name = name_make(text)

    text = Image.open(name).resize((600, 350))
    bg = Image.open('assets/img/batman_logo_bg_1200.jpg').resize((600, 350))

    img.paste(bg, (300, 175), text)

    img.save(name)

    return name

