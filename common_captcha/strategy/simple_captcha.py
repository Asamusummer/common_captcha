#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import os
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from common_captcha.utils.redis_util import init_redis
from common_captcha.utils.uuid_util import generate_uuid
from common_captcha.utils.ramdom_util import (
    generate_random_background_color,
    generate_code_chr,
)


class SimpleCaptcha:
    """ 简单验证码 """

    @staticmethod
    def get_font_size_resource() -> os.path:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'fonts',
                            'WenQuanZhengHei.ttf')

    @staticmethod
    def generate_background_size_picture(width: int = 120, height: int = 35) -> Image:
        """ 生成制定大小背景图 """

        return Image.new('RGB', (width, height), generate_random_background_color())

    @staticmethod
    def draw_code(font_size: int = 35, code_length: int = 4, width: int = 120, height: int = 35):
        """ 画验证码 """

        im = SimpleCaptcha.generate_background_size_picture(width, height)
        dio = ImageDraw.Draw(im)
        font_family = ImageFont.truetype(SimpleCaptcha.get_font_size_resource(), size=font_size)
        temp = []
        for i in range(code_length):
            random_code_str = generate_code_chr()
            dio.text((10 + i * 30, -2), random_code_str, generate_random_background_color(), font=font_family)
            temp.append(random_code_str)
        return ''.join(temp), im

    @classmethod
    def noise(cls, image, width=120, height=35, line_count=3, point_count=20) -> Image:
        """

        :param image: 图片对象
        :param width: 图片宽度
        :param height: 图片高度
        :param line_count: 线条数量
        :param point_count: 点的数量
        :return:
        """
        draw = ImageDraw.Draw(image)
        for i in range(line_count):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=generate_random_background_color())

            # 画点
            for i in range(point_count):
                draw.point([random.randint(0, width), random.randint(0, height)],
                           fill=generate_random_background_color())
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.arc((x, y, x + 4, y + 4), 0, 90, fill=generate_random_background_color())
        return image

    @classmethod
    def get_code_with_base64_string(
            cls, font_size: int = 35, code_length: int = 4,
            width: int = 120, height: int = 35, need_noise: bool = True) -> str:
        token = generate_uuid()
        code, im = cls.draw_code(font_size, code_length, width, height)
        if need_noise:
            im = cls.noise(im)
        f = BytesIO()
        im.save(f, 'png')
        im.save('./code.png')
        data = f.getvalue()
        f.close()
        encode_data = base64.b64encode(data)
        data = str(encode_data, encoding='utf-8')
        img_data = "data:image/jpeg;base64,{data}".format(data=data)

        cache_key = f'SimpleCaptcha:{token}'
        init_redis().setex(cache_key, code, 6000)
        return img_data

    @classmethod
    def verify(cls, params: str, token: str):
        cache_key = f'SimpleCaptcha:{token}'
        base64.b64decode(params.encode()).decode()
        pass


if __name__ == '__main__':
    print(SimpleCaptcha.get_code_with_base64_string())
