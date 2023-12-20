==============
common-captcha
==============

common-captcha 验证码程序，包括简单验证码和滑块验证码，基于用户行为验证

Features
====================================

- 简单验证码
- 滑动拼图验证码

Introduction
====================================

Install with pip:

.. code-block:: console

    $ pip install common-captcha

Preview
====================================

滑块验证码

.. image:: https://gitee.com/anji-plus/captcha/raw/master/images/%E6%BB%91%E5%8A%A8%E6%8B%BC%E5%9B%BE.gif

How To Use?
====================================

在此之前，你需要准备一个可用的redis

.. code-block:: console

    redis_url redis://xxxxxx:xxxxxx@xxxxx:xxx/11


Configuration
====================================

.. code-block:: python

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


当你需要针对定制化配置操作时，你需要重写对应的属性信息，并传入对应的验证码中：demo

.. code-block:: python

    from common_captcha.config import BlockPuzzleCaptchaConfig as _baseConfig

    class BlockPuzzleCaptchaConfig(_baseConfig):
        font_water_text_font_size = 30
        font_water_text = "中国传媒大学"


简单验证码:

.. code-block:: python

    from common_captcha.strategy.simple_captcha import SimpleCaptcha

    simple_captcha = SimpleCaptcha(redis_url="redis://xxxxxx:xxxxxx@xxxxx:xxx/11", configs=BlockPuzzleCaptchaConfig)
    print(simple_captcha.get())
    print(simple_captcha.verify({"token": "", "code": ""}))


滑块验证码:

.. code-block:: python

    from common_captcha.strategy.block_puzzle_captcha import BlockPuzzleCaptcha

    block_captcha = BlockPuzzleCaptcha(redis_url="redis://xxxxxx:xxxxxx@xxxxx:xxx/11")
    print(block_captcha.get())
    print(block_captcha.verify(token="", point_json={"x": "", "y": ""}))

