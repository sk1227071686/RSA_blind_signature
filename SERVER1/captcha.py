import random

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_check_code():

    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO

    img = Image.new('RGB', (236, 36), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\Verdana.TTF', size=30)

    random_check_code = ''
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 20 + 15, 4), random_char,font=font)
        random_check_code += random_char

    width = 236
    height = 36
    for i in range(8):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(36):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    f = BytesIO()
    img.save(f,'png')
    #print(type(img))
    data = f.getvalue()
    return data,random_check_code
if __name__ == '__main__':
    data,code=generate_check_code()
    print(code)
    with open('chapter.png','wb') as f:
        f.write(data)