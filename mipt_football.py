import os
from time import strftime, localtime, tzset
from scoreboard import Scoreboard

os.environ['TZ'] = 'Europe/Moscow'
tzset()


class MIPTFootball(Scoreboard):
    # Image size
    size_x = 600
    size_y = 470

    # Parameters of black blocks
    block_width = 266
    block_height = 151
    block_margin_lr = 21
    block_margin_b = 64

    title_padding_top = 15
    title_line_spacing = 10

    fonts = {
        'title': ('assets/pt_sans_caption.ttf', 58),
        'subtitle': ('assets/pt_sans.ttf', 25),
        'team': ('assets/pt_sans_caption.ttf', 40),
        'timestamp': ('assets/pt_sans.ttf', 16),
        'digits': ('assets/ds-digib.ttf', 180),
    }

    colours = {
        'text': (0, 0, 0),
        'block': (0, 0, 0),
        'bg': (255, 255, 255),
        'score': (255, 255, 0)
    }

    @staticmethod
    def timestamp():
        return 'Обновлено в %s' % strftime('%H:%M', localtime())


if __name__ == '__main__':

    game = {
        'title': 'Матч Века',
        'subtitle': '21-22 мая 2016 г.',
        'contestants': [
            ('assets/teams/frtk.png', 'ФРТК'),
            ('assets/teams/fopf.png', 'ФОПФ')
        ],
    }

    with MIPTFootball(**game) as img:
        with open('mipt.png', 'wb') as f:
            img.draw_template()
            img.draw_score([67, 83])
            # img.draw_timestamp()
            img.save(f)
