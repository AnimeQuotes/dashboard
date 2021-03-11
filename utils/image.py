from io import BytesIO
from typing import Union, List

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont


IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 512

CHARACTER_WIDTH = 360

DRAW_WIDTH = IMAGE_WIDTH - CHARACTER_WIDTH
DRAW_X = CHARACTER_WIDTH

QUOTE_MARGIN = 30
QUOTE_WIDTH = DRAW_WIDTH - QUOTE_MARGIN
QUOTE_FONT = ImageFont.truetype("arialbi", 34)
QUOTE_FONT_ = TTFont(QUOTE_FONT.path)

AUTHOR_MARGIN = 10
AUTHOR_FONT = ImageFont.truetype("arial", 24)


def sanitize_text(text: str) -> str:
    output = ""
    tables = QUOTE_FONT_["cmap"].tables
    for c in text:
        for table in tables:
            if ord(c) in table.cmap:
                output += c
                break

    return output


def text_wrap(text: str) -> List[dict]:
    width, height = QUOTE_FONT.getsize(text)
    if width <= QUOTE_WIDTH:
        return [{"width": width, "height": height, "text": text}]
    else:
        lines = []
        current_line = ""
        words = text.split()
        total_words = len(words)

        for i, word in enumerate(words, 1):
            line_width, line_height = QUOTE_FONT.getsize(current_line + (" " if current_line else "") + word)
            if line_width < QUOTE_WIDTH:
                current_line += (" " if current_line else "") + word

                if i == total_words:
                    lines.append({"width": line_width, "height": line_height, "text": current_line})
            else:
                line_width, line_height = QUOTE_FONT.getsize(current_line)
                lines.append({"width": line_width, "height": line_height, "text": current_line})
                current_line = word

        return lines


def generate_quote_image(*, author: str, quote: str, image_path: str) -> Union[str, BytesIO]:
    canvas = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    character = Image.open(image_path).resize((CHARACTER_WIDTH, IMAGE_HEIGHT))
    canvas.paste(character, (0, 0))

    draw = ImageDraw.Draw(canvas)

    clean_text = sanitize_text(quote)
    if not clean_text:
        return "Quote text does not have valid characters supported by the font."

    lines = text_wrap(clean_text)
    line_y = (IMAGE_HEIGHT - sum(line["height"] for line in lines)) / 2
    for line in lines:
        line_x = DRAW_X + ((DRAW_WIDTH - line["width"]) / 2)
        draw.text((line_x, line_y), line["text"], font=QUOTE_FONT)
        line_y += line["height"]

    author = "- " + author
    author_w, author_h = AUTHOR_FONT.getsize(author)
    author_x = DRAW_X + ((DRAW_WIDTH - author_w) / 2)
    draw.text((author_x, IMAGE_HEIGHT - AUTHOR_MARGIN - author_h), author, font=AUTHOR_FONT)

    io = BytesIO()
    canvas.save(io, format="png")
    io.seek(0)

    return io
