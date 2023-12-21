#!/usr/bin/env python
from __future__ import annotations

__author__ = "lei.wang"
import os
import json
from common_captcha import BASE_DIR
from common_captcha.utils.redis_util import RedisUtil
from common_captcha.utils.image_util import ImageUtil, open_image, image_to_rgba, set_art_text
from common_captcha.utils.ramdom_util import generate_random_int
from common_captcha.utils.uuid_util import generate_uuid
from common_captcha.config import ClickWordCaptchaConfig


class ClickWordCaptcha:
    """ 点击文字行为验证码 """

    base64_image_prefix = "data:image/jpeg;base64,{data}"
    _data_encoding = "utf-8"

    def __init__(self, redis_url: str = None, configs: ClickWordCaptchaConfig = ClickWordCaptchaConfig) -> None:
        self.redis = RedisUtil(redis_url=redis_url)
        self.background_image_list = list()
        self.__init_configs(configs)
        self.set_up()

    def __init_configs(self, configs: ClickWordCaptchaConfig = ClickWordCaptchaConfig) -> None:
        if not configs:
            self.click_word_captcha_cache_key = ClickWordCaptchaConfig.click_word_captcha_cache_key
            self.click_word_captcha_cache_key_expire = ClickWordCaptchaConfig.click_word_captcha_cache_key_expire
            self.font_ttf_root_path = ClickWordCaptchaConfig.font_ttf_root_path
            self.click_word_captcha_font_number = ClickWordCaptchaConfig.click_word_captcha_font_number
            self.click_word_captcha_text = ClickWordCaptchaConfig.click_word_captcha_text
            self.click_word_captcha_font_size = ClickWordCaptchaConfig.click_word_captcha_font_size
            self.background_image_root_path = ClickWordCaptchaConfig.background_image_root_path
        self.click_word_captcha_cache_key = configs.click_word_captcha_cache_key
        self.click_word_captcha_cache_key_expire = configs.click_word_captcha_cache_key_expire
        self.font_ttf_root_path = configs.font_ttf_root_path
        self.click_word_captcha_font_number = configs.click_word_captcha_font_number
        self.click_word_captcha_text = configs.click_word_captcha_text
        self.click_word_captcha_font_size = configs.click_word_captcha_font_size
        self.background_image_root_path = configs.background_image_root_path
        return None

    def set_up(self) -> None:
        backgroundImageRoot = self.get_resources(self.background_image_root_path)

        def process_file(res, path, info=None, err=None):
            if os.path.isdir(path):
                return
            res.append(path)

        for root, dirs, files in os.walk(backgroundImageRoot):
            for file in files:
                path = os.path.join(root, file)
                process_file(self.background_image_list, path)
        return None

    def get_resources(self, path_str: str) -> os.path:
        return os.path.join(BASE_DIR, path_str)

    def get_background_image(self) -> ImageUtil:
        max = len(self.background_image_list) - 1
        if max <= 0:
            max = 1
        src = self.background_image_list[generate_random_int(0, max)]
        src_image = open_image(src)
        image_util_obj = ImageUtil(
            src=src,
            src_image=src_image,
            rgba_image=image_to_rgba(src_image),
            width=src_image.size[0],
            height=src_image.size[1],
            font_path=self.get_resources(self.font_ttf_root_path),
        )
        return image_util_obj

    def get_random_words(self, word_count: int) -> list:
        word_list = []
        word_set = set()
        list_words = list(self.click_word_captcha_text)
        length = len(list_words)
        while True:
            word = list_words[generate_random_int(0, length - 1)]
            word_set.add(word)
            if len(word_set) >= word_count:
                for w in word_set:
                    word_list.append(w)
                break
        return word_list

    def random_word_points(self, width: int, height: int, i: int, count: int) -> dict:
        avg_width = width / (count + 1)
        font_size_half = self.click_word_captcha_font_size / 2
        x = y = 0
        if avg_width < font_size_half:
            x = generate_random_int(int(1+font_size_half), int(width))
        else:
            if i == 0:
                x = generate_random_int(int(1+font_size_half), int(avg_width*(i+1)-font_size_half))
            else:
                x = generate_random_int(int(avg_width*i+font_size_half), int(avg_width*(i+1)-font_size_half))
        y = generate_random_int(int(self.click_word_captcha_font_size), int(height-font_size_half))
        return {"x": x, "y": y}

    def get_image_data(self, background_image: ImageUtil) -> tuple:
        word_count = self.click_word_captcha_font_number

        num = generate_random_int(1, word_count)
        current_words = self.get_random_words(word_count)

        points_list = []
        word_list = []

        i = 0
        for _, word in enumerate(current_words):
            point = self.random_word_points(background_image.width, background_image.height, i, word_count)
            set_art_text(background_image, word, self.click_word_captcha_font_size, point)

            if num - 1 != i:
                points_list.append(point)
                word_list.append(word)

            i = i+1

        return points_list, word_list

    def get_cache_key(self, token: str) -> str:
        return f"{self.click_word_captcha_cache_key}:{token}"

    def get(self) -> dict:
        result = {}
        background_image = self.get_background_image()
        points_list, word_list = self.get_image_data(background_image=background_image)
        background_image_base64_string = background_image.base64_encode_image(background_image.rgba_image)
        result["originalImageBase64"] = self.base64_image_prefix.format(data=background_image_base64_string)
        result["word_lists"] = word_list
        result["token"] = generate_uuid()
        cache_key = self.get_cache_key(result["token"])
        self.redis.set(cache_key, json.dumps(points_list), self.click_word_captcha_cache_key_expire)
        return result

    def check(self, token: str, point_jsons: list) -> bool:
        cache_key = self.get_cache_key(token)
        cache_value_bytes = self.redis.get(cache_key)
        if not cache_value_bytes:
            return False

        cache_value = json.loads(cache_value_bytes.decode(self._data_encoding))

        for index, point in enumerate(cache_value):
            target_point = point_jsons[index]
            font_size = self.click_word_captcha_font_size
            if (
                target_point.get("x")-font_size > point.get("x") or
                target_point.get("x") > point.get("x")+font_size or
                target_point.get("y")-font_size > point.get("y") or
                target_point.get("y") > point.get("y")+font_size
            ):
                return False
        return True

    def verify(self, token: str, point_jsons: list) -> bool:
        flag = self.check(token, point_jsons)
        if not flag:
            return False
        cache_key = self.get_cache_key(token)
        self.redis.delete(cache_key)
        return True


if __name__ == '__main__':
    click_captcha = ClickWordCaptcha(redis_url="redis://xxxxxx:xxxxxx@xxxxx:xxx/11")
    # print(click_captcha.get())
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
