==============
common_captcha
==============

验证码程序，包括简单验证码和滑块验证码

Introduction
====================================

Install with pip:

.. code-block:: console

    $ python -m pip install common-captcha


How To Use?
====================================

在此之前，你需要准备一个可用的redis

.. code-block:: console

    redis_url redis://xxxxxx:xxxxxx@xxxxx:xxx/11


简单验证码:

.. code-block:: python

    from common_captcha.strategy.simple_captcha import SimpleCaptcha

    simple_captcah = SimpleCaptcha(redis_url="redis://xxxxxx:xxxxxx@xxxxx:xxx/11")
    print(simple_captcah.get())
    print(simple_captcah.verify({"token": "", "code": ""}))


滑块验证码:

.. code-block:: python

    from common_captcha.strategy.block_puzzle_captcha import BlockPuzzleCaptcha

    block_captcha = BlockPuzzleCaptcha(redis_url="redis://xxxxxx:xxxxxx@xxxxx:xxx/11")
    print(block_captcha.get())
    print(block_captcha.verify(token="", point_json={"x": "", "y": ""}))

