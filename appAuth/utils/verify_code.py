import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def check_code(width=120, height=30, char_length=5, font_file='Monaco.ttf', font_size=28):
    code=[]
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    def rndChar():
        return chr(random.randint(65, 90))

    def rndColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(1, 4)
        draw.text((width * i / char_length, h), char, font=font, fill=rndColor())

    for i in range(50):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=rndColor())

    for i in range(3):
        draw.line((random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)), fill=rndColor())

    for i in range(4):
        draw.arc((random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)), 0, 90, fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)

