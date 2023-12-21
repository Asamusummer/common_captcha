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

https://github.com/Asamusummer/common_captcha/blob/main/%E6%BB%91%E5%8A%A8%E6%8B%BC%E5%9B%BE.gif


点击文字验证

https://github.com/Asamusummer/common_captcha/blob/main/%E7%82%B9%E9%80%89%E6%96%87%E5%AD%97.gif


How To Use?
====================================

在此之前，你需要准备一个可用的redis

.. code-block:: console

    redis_url redis://xxxxxx:xxxxxx@xxxxx:xxx/11


Configuration
====================================

.. code-block:: python

    class SimpleCaptchaConfig(BaseConfig):
        """ 简单验证码配置 """

        simple_captcha_cache_key = "SimpleCaptcha"  # simple captcha redis cache key
        simple_captcha_cache_key_expire = 6000  # simple captcha redis cache key expired time


    class BlockPuzzleCaptchaConfig(BaseConfig):
        """ 滑块验证码配置 """

        block_puzzle_captcha_cache_key = "BlockPuzzleCaptcha"  # block puzzle captcha redis cache key
        block_puzzle_captcha_cache_key_expire = 6000  # block puzzle captcha redis cache key expired time
        block_puzzle_captcha_check_offsetX = 10  # block puzzle captcha verify offset x
        background_image_root_path = "resource/defaultImages/jigsaw/original"  # block puzzle background images
        template_image_root_path = "resource/defaultImages/jigsaw/slidingBlock"  # block puzzle template images
        pic_click_root_path = "resource/defaultImages/pic-click"  # block puzzle pic check images
        font_ttf_root_path = "resource/fonts/WenQuanZhengHei.ttf"  # block puzzle font.ttf
        font_water_text = "lei.wang"  # block puzzle captcha water text
        font_water_text_font_size = 22  # block puzzle captcha water text font size


    class ClickWordCaptchaConfig(BaseConfig):
        """ 文字点击验证码配置 """

        click_word_captcha_cache_key = "ClickWordCaptcha"  # click word captcha redis cache key
        click_word_captcha_cache_key_expire = 6000  # click_word_captcha_cache_key expired time
        font_ttf_root_path = "resource/fonts/WenQuanZhengHei.ttf"  # click word captcha font.ttf
        click_word_captcha_font_number = 4
        click_word_captcha_font_size = 25
        background_image_root_path = "resource/defaultImages/jigsaw/original"  # click word captcha background images
        click_word_captcha_text = "的一了是我不在人们有来他这上着个地到大里说就去子得也和那要下看天时过出小么起你都把好还多没为又可家学只以主会样年想生同老中十从自面前头道它后然走很像见两用她国动进成回什边作对开而己些现山民候经发工向事命给长水几义三声于高手知理眼志点心战二问但身方实吃做叫当住听革打呢真全才四已所敌之最光产情路分总条白话东席次亲如被花口放儿常气五第使写军吧文运再果怎定许快明行因别飞外树物活部门无往船望新带队先力完却站代员机更九您每风级跟笑啊孩万少直意夜比阶连车重便斗马哪化太指变社似士者干石满日决百原拿群究各六本思解立河村八难早论吗根共让相研今其书坐接应关信觉步反处记将千找争领或师结块跑谁草越字加脚紧爱等习阵怕月青半火法题建赶位唱海七女任件感准张团屋离色脸片科倒睛利世刚且由送切星导晚表够整认响雪流未场该并底深刻平伟忙提确近亮轻讲农古黑告界拉名呀土清阳照办史改历转画造嘴此治北必服雨穿内识验传业菜爬睡兴形量咱观苦体众通冲合破友度术饭公旁房极南枪读沙岁线野坚空收算至政城劳落钱特围弟胜教热展包歌类渐强数乡呼性音答哥际旧神座章帮啦受系令跳非何牛取入岸敢掉忽种装顶急林停息句区衣般报叶压慢叔背细"


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

点击文字验证码:

.. code-block:: python

    from common_captcha.strategy.click_word_captcha import ClickWordCaptcha

    click_captcha = ClickWordCaptcha(redis_url="redis://xxxxxx:xxxxxx@xxxxx:xxx/11")
    token = "2a6d0134672845469904d9d541c93f60"
    point_jsons = [
        {
            "x": 17,
            "y": 187
        },
        {
            "x": 140,
            "y": 43
        },
        {
            "x": 193,
            "y": 64
        }
    ]
    print(click_captcha.verify(token, point_jsons))

