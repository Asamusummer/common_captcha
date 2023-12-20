#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations

import base64
import os
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from common_captcha.utils.redis_util import RedisUtil
from common_captcha.utils.uuid_util import generate_uuid
from common_captcha.utils.ramdom_util import generate_random_background_color, generate_code_chr


class SimpleCaptcha:
    """ 简单验证码 """

    simple_captcha_cache_key = "SimpleCaptcha"
    simple_captcha_cache_key_expire = 6000
    base64_image_prefix = "data:image/jpeg;base64,{data}"
    base64_image__type = "png"
    _data_encoding = "utf-8"

    def __init__(self, redis_url: str = None):
        self.redis = RedisUtil(redis_url=redis_url)

    @staticmethod
    def get_font_size_resource() -> os.path:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resource', 'fonts',
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

    def get_cache_key(self, token: str) -> str:
        return f'{self.simple_captcha_cache_key}:{token}'

    def get(self, font_size: int = 35, code_length: int = 4, width: int = 120,
                                    height: int = 35, need_noise: bool = False) -> dict:
        token = generate_uuid()
        code, im = self.draw_code(font_size, code_length, width, height)
        if need_noise:
            im = self.noise(im)
        f = BytesIO()
        im.save(f, self.base64_image__type)
        data = f.getvalue()
        f.close()
        encode_data = base64.b64encode(data)
        data = str(encode_data, encoding=self._data_encoding)
        img_data = self.base64_image_prefix.format(data=data)
        cache_key = self.get_cache_key(token)
        self.redis.setex(cache_key, code, self.simple_captcha_cache_key_expire)
        return {"base64ImageString": img_data, "token": token}

    def verify(self, params: dict) -> bool:
        token = params.get("token") or ""
        code = params.get("code") or ""

        cache_key = self.get_cache_key(token)
        cache_value_bytes = self.redis.get(cache_key)
        if not cache_value_bytes:
            return False
        if cache_value_bytes.decode() == code:
            self.redis.delete(cache_key)
            return True
        return False


if __name__ == '__main__':
    simple_captcha = SimpleCaptcha(redis_url="redis://:O82cW8c8Qz@172.16.211.111:30180/11")
    print(simple_captcha.get())
    # print(simple_captcha.verify({"token": "99aae7ca742c42bb884a2d7d898b589d", "code": "z8o5"}))
