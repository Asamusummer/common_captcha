#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations

import base64
import os
from io import BytesIO
from PIL import ImageFont, ImageDraw, Image
from common_captcha import BASE_DIR


class ImageUtil:
    """ 图像处理工具类 """

    _data_encoding = "utf-8"
    _data_img_type = "PNG"

    def __init__(self, src, src_image, rgba_image, font_path, width, height):
        self.src = src
        self.src_image = src_image
        self.rgba_image = rgba_image
        self.font_path = font_path
        self.width = width
        self.height = height

    def set_text(self, image,  text, font_size, font_color) -> None:
        font = ImageFont.truetype(self.font_path, font_size)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=font_color)
        return None

    def set_rgba(self, rgba_image, x, y, c):
        ps = rgba_image.load()
        ps[x, y] = c

    def base64_encode_image(self, image):
        # 创建一个内存缓冲区
        buffer = BytesIO()
        # 将图像保存到缓冲区
        image.save(buffer, format=self._data_img_type)
        # 获取缓冲区中的字节数据
        image_bytes = buffer.getvalue()
        # 将字节数据进行base64编码
        base64_encoded_image = base64.b64encode(image_bytes).decode(self._data_encoding)
        return base64_encoded_image


def image_to_rgba(img: Image):
    # 如果图像已经是RGBA格式，则无需转换
    if img.mode == "RGBA":
        return img

    # 创建一个新的RGBA图像
    rgba_img = Image.new("RGBA", img.size)

    # 使用ImageDraw模块将原始图像绘制到新的RGBA图像上
    draw = ImageDraw.Draw(rgba_img)
    draw.bitmap((0, 0), img, fill=(255, 255, 255, 255))
    return rgba_img


def open_image(src: str) -> Image:
    image = Image.open(src)
    return image


def is_opcacity(rgba_image, x, y) -> bool:
    """ 判断图像是否透明 """

    return rgba_image.getpixel((x, y))[3] <= 125


def get_font_path() -> str:
    return os.path.join(BASE_DIR, "resource/fonts/WenQuanZhengHei.ttf")


def set_art_text(background_image: ImageUtil, word: str, font_size: int, point: dict) -> None:

    font = ImageFont.truetype(get_font_path(), font_size)
    rgba_image = ImageDraw.Draw(background_image.rgba_image)
    rgba_image.text((point.get("x"), point.get("y")), word, font=font)
    return None
