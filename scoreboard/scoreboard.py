from typing import Sequence
from PIL import Image, ImageDraw, ImageFont


class Scoreboard:
    contestants = title = subtitle = timestamp = None
    size_x = size_y = None
    block_width = block_height = block_margin_lr = block_margin_b = None
    colours = None
    title_line_spacing = title_padding_top = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        self.fonts = {name: ImageFont.truetype(*font)
                      for name, font in self.fonts.items()}

        self.image = Image.new('RGBA', (self.size_x, self.size_y),
                               self.colours['bg'])
        self.draw = ImageDraw.Draw(self.image)

        # Score boxes
        b1_x0 = self.block_margin_lr
        b1_y0 = self.size_y - self.block_height - self.block_margin_b
        b1_y0 -= 0 if self.title else 45
        b1_x1 = b1_x0 + self.block_width - 1
        b1_y1 = b1_y0 + self.block_height - 1

        b2_x0 = self.size_x - self.block_width - self.block_margin_lr
        b2_y0 = b1_y0
        b2_x1 = b2_x0 + self.block_width - 1
        b2_y1 = b1_y1

        self.bcs = [(b1_x0, b1_y0, b1_x1, b1_y1), (b2_x0, b2_y0, b2_x1, b2_y1)]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _center_text(text, font, box):
        by_lt = by_rb = None

        if len(box) == 4:
            bx_lt, by_lt, bx_rb, by_rb = box
        elif len(box) == 2:
            if type(box[0]) is not int:
                (bx_lt, by_lt), (bx_rb, by_rb) = box
            else:
                bx_lt, bx_rb = box
        else:
            raise ValueError('Invalid box value')

        w, h = font.font.getsize(text)[0]

        return (
            bx_lt + (bx_rb - bx_lt - w) / 2,
            None if (by_lt is None) else (by_lt + (by_rb - by_lt - h) / 2)
        )

    def _draw_text(self, xy, text: str, fill, font):
        x, y = xy
        off_x, off_y = font.getoffset(text)
        top_left = (x-off_x, y-off_y)
        self.draw.text(top_left, text, fill=fill, font=font)

        # TODO: debug
        # s = font.font.getsize(text)[0]
        # self.draw.rectangle(((x, y), (x+s[0], y+s[1])), outline=(255, 0, 0))

        return top_left[1] + font.getsize('M')[1]

    def draw_template(self):

        colours = self.colours

        # Black blocks
        for p in self.bcs:
            self.draw.rectangle(p, colours['block'], colours['block'])

        baseline = 0

        if self.title:
            t_font = self.fonts['title']

            t_x, _ = self._center_text(self.title, t_font, (0, self.size_x))
            t_y = self.title_padding_top

            baseline = self._draw_text((t_x, t_y),
                                       self.title, colours['text'], t_font)

        if self.subtitle:
            st_font = self.fonts['subtitle']
            st_x, _ = self._center_text(self.subtitle, st_font,
                                        (0, self.size_x))
            st_y = baseline + self.title_line_spacing

            baseline = self._draw_text((st_x, st_y),
                                       self.subtitle, colours['text'], st_font)

        # Teams
        for i, (bc, (logo, name)) in enumerate(zip(self.bcs, self.contestants)):
            bx_lt, by_lt, bx_rb, by_rb = bc
            bw = bx_rb - bx_lt

            # Team name
            t_x, _ = self._center_text(name, self.fonts['team'], (bx_lt, bx_rb))
            t_y = by_rb + 10

            self.draw.text((t_x, t_y), name, colours['text'],
                           font=self.fonts['team'])

            # Team logo
            im = Image.open(logo)
            im.thumbnail((bw, (by_lt - baseline)*0.8), Image.ANTIALIAS)

            l_x = bx_lt + int((bw - im.size[0])/2)
            l_y = baseline + int((by_lt - baseline - im.size[1])/2)
            self.image.paste(im, box=(l_x, l_y))

    def draw_score(self, score: Sequence[int]):
        font = self.fonts['digits']

        for bc, value in zip(self.bcs, map(str, score)):
            x, y = self._center_text(value, font, bc)
            self._draw_text((x, y), value, self.colours['score'], font=font)

    def draw_timestamp(self):
        timestamp = self.timestamp()

        font = self.fonts['timestamp']
        t_w, t_h = font.font.getsize(timestamp)[0]

        self.draw.text((self.size_x - 10 - t_w, self.size_y - 10 - t_h),
                       timestamp, self.colours['text'], font=font)

    def save(self, fp):
        self.image.save(fp, format='png', optimize=True)
