from PIL import Image, ImageDraw, ImageFont

width, height = 480, 20
text = "CakeCTF{fd408e00d5824d7220c4d624f894144e}"

img = Image.new('1', (width, height), 'white')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/robotomono/RobotoMono-Regular.ttf", size=19
)

tw, th = draw.textsize(text, font=font)
x = (width - tw) // 2
y = (height - th) // 2
draw.text((x, y), text, font=font, fill="black")

img.save("flag.png")
