#!/usr/bin/env python
from __future__ import annotations

__author__ = "lei.wang"


class SimpleCaptchaConfig:
    """ 简单验证码配置 """

    simple_captcha_cache_key = "SimpleCaptcha"  # simple captcha redis cache key
    simple_captcha_cache_key_expire = 6000  # simple captcha redis cache key expired time


class BlockPuzzleCaptchaConfig:
    """ 滑块验证码配置 """

    block_puzzle_captcha_cache_key = "BlockPuzzleCaptcha"   # block puzzle captcha redis cache key
    block_puzzle_captcha_cache_key_expire = 6000    # block puzzle captcha redis cache key expired time
    block_puzzle_captcha_check_offsetX = 10     # block puzzle captcha verify offset x
    background_image_root_path = "resource/defaultImages/jigsaw/original"   # block puzzle background images
    template_image_root_path = "resource/defaultImages/jigsaw/slidingBlock"  # block puzzle template images
    pic_click_root_path = "resource/defaultImages/pic-click"    # block puzzle pic check images
    font_ttf_root_path = "resource/fonts/WenQuanZhengHei.ttf"   # block puzzle font.ttf
    font_water_text = "lei.wang"    # block puzzle captcha water text
    font_water_text_font_size = 22  # block puzzle captcha water text font size
