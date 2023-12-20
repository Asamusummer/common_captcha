#!/usr/bin/env python
from __future__ import annotations

__author__ = "lei.wang"
import os
import json
from common_captcha import BASE_DIR
from common_captcha.utils.redis_util import RedisUtil
from common_captcha.utils.ramdom_util import generate_random_int
from common_captcha.utils.image_util import ImageUtil, image_to_rgba, open_image, is_opcacity
from common_captcha.utils.uuid_util import generate_uuid
from common_captcha.config import BlockPuzzleCaptchaConfig


class BlockPuzzleCaptcha:
    """ 滑块拼图验证码 """

    base64_image_prefix = "data:image/jpeg;base64,{data}"
    _data_encoding = "utf-8"

    def __init__(self, redis_url: str = None, configs=None):
        self.redis = RedisUtil(redis_url=redis_url)
        self.__init_configs(configs)
        self.background_image_list = list()
        self.template_image_root = list()
        self.click_background_image_root = list()
        self.points = dict()
        self.set_up()

    def __init_configs(self, configs: BlockPuzzleCaptchaConfig = None) -> None:
        if not configs:
            self.block_puzzle_captcha_cache_key = BlockPuzzleCaptchaConfig.block_puzzle_captcha_cache_key
            self.block_puzzle_captcha_cache_key_expire = BlockPuzzleCaptchaConfig.block_puzzle_captcha_cache_key_expire
            self.block_puzzle_captcha_check_offsetX = BlockPuzzleCaptchaConfig.block_puzzle_captcha_check_offsetX
            self.background_image_root_path = BlockPuzzleCaptchaConfig.background_image_root_path
            self.template_image_root_path = BlockPuzzleCaptchaConfig.template_image_root_path
            self.pic_click_root_path = BlockPuzzleCaptchaConfig.pic_click_root_path
            self.font_ttf_root_path = BlockPuzzleCaptchaConfig.font_ttf_root_path
            self.font_water_text = BlockPuzzleCaptchaConfig.font_water_text
            self.font_water_text_font_size = BlockPuzzleCaptchaConfig.font_water_text_font_size
            return None
        self.block_puzzle_captcha_cache_key = configs.block_puzzle_captcha_cache_key
        self.block_puzzle_captcha_cache_key_expire = configs.block_puzzle_captcha_cache_key_expire
        self.block_puzzle_captcha_check_offsetX = configs.block_puzzle_captcha_check_offsetX
        self.background_image_root_path = configs.background_image_root_path
        self.template_image_root_path = configs.template_image_root_path
        self.pic_click_root_path = configs.pic_click_root_path
        self.font_ttf_root_path = configs.font_ttf_root_path
        self.font_water_text = configs.font_water_text
        self.font_water_text_font_size = configs.font_water_text_font_size
        return None

    def get_resources(self, path_str: str) -> os.path:
        return os.path.join(BASE_DIR, path_str)

    def set_up(self) -> None:
        backgroundImageRoot = self.get_resources(self.background_image_root_path)
        templateImageRoot = self.get_resources(self.template_image_root_path)
        clickBackgroundImageRoot = self.get_resources(self.pic_click_root_path)

        def process_file(res, path, info=None, err=None):
            if os.path.isdir(path):
                return
            res.append(path)

        for root, dirs, files in os.walk(backgroundImageRoot):
            for file in files:
                path = os.path.join(root, file)
                process_file(self.background_image_list, path)

        for root, dirs, files in os.walk(templateImageRoot):
            for file in files:
                path = os.path.join(root, file)
                process_file(self.template_image_root, path)

        for root, dirs, files in os.walk(clickBackgroundImageRoot):
            for file in files:
                path = os.path.join(root, file)
                process_file(self.click_background_image_root, path)

        return None

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

    def get_template_image(self) -> ImageUtil:
        max = len(self.template_image_root) - 1
        if max <= 0:
            max = 1
        src = self.template_image_root[generate_random_int(0, max)]
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

    def generate_picture_points(self, background_image: ImageUtil, template_image: ImageUtil) -> None:
        x, y = 0, 0
        width_diff = background_image.width - template_image.width
        height_diff = background_image.height - template_image.height

        if width_diff <= 0:
            x = 5
        else:
            x = generate_random_int(100, width_diff - 100)

        if height_diff <= 0:
            y = 5
        else:
            y = generate_random_int(5, height_diff)

        self.points = {'x': x, 'y': y, 'secretKey': generate_uuid()}
        return None

    def cut_by_template(self, background_image: ImageUtil, template_image: ImageUtil, x1: float, y1: float) -> None:
        x_length = template_image.width
        y_length = template_image.height

        for x in range(0, x_length):
            for y in range(0, y_length):
                # 如果模板图像当前像素点不是透明色 copy源文件信息到目标图片中
                is_opacity = is_opcacity(template_image.rgba_image, x, y)

                background_x = x + x1
                background_y = y + y1

                if not is_opacity:
                    # 获取原图像素
                    background_image_rgba = background_image.rgba_image.getpixel((background_x, background_y))
                    # 将原图的像素扣到模板图上
                    template_image.rgba_image.putpixel((x, y), background_image_rgba)
                    # # 背景图区域模糊
                    background_image.rgba_image.putpixel((background_x, background_y), (105, 105, 105))

                if x == (x_length - 1) or y == (y_length - 1):
                    continue

                right_opcacity = is_opcacity(template_image.rgba_image, x + 1, y)
                bottom_opcacity = is_opcacity(template_image.rgba_image, x, y + 1)

                # 描边处理，,取带像素和无像素的界点，判断该点是不是临界轮廓点,如果是设置该坐标像素是白色
                if (
                        (is_opacity and not right_opcacity) or
                        (not is_opacity and right_opcacity) or
                        (is_opacity and not bottom_opcacity) or
                        (not is_opacity and bottom_opcacity)
                ):
                    template_image.set_rgba(template_image.rgba_image, x, y, (0xff, 0xff, 0xff, 0xff))
                    background_image.set_rgba(background_image.rgba_image, background_x, background_y, (0xff, 0xff, 0xff, 0xff))
        return None

    def interference_by_template(self, background_image: ImageUtil, template_image: ImageUtil, x1: float, y1: float) -> None:
        x_length = template_image.width
        y_length = template_image.height

        for x in range(0, x_length):
            for y in range(0, y_length):
                # 如果模板图像当前像素点不是透明色 copy源文件信息到目标图片中
                is_opacity = is_opcacity(template_image.rgba_image, x, y)
                background_x = x + x1
                background_y = y + y1

                if not is_opacity:
                    background_image.rgba_image.putpixel((background_x, background_y), (105, 105, 105))

                if x == (x_length - 1) or y == (y_length - 1):
                    continue

                right_opcacity = is_opcacity(template_image.rgba_image, x + 1, y)
                bottom_opcacity = is_opcacity(template_image.rgba_image, x, y + 1)
                if (
                        (is_opacity and not right_opcacity) or
                        (not is_opacity and right_opcacity) or
                        (is_opacity and not bottom_opcacity) or
                        (not is_opacity and bottom_opcacity)
                ):
                    background_image.set_rgba(background_image.rgba_image, background_x, background_y, (0xff, 0xff, 0xff, 0xff))
        return None

    def picture_templates_cut(self, background_image: ImageUtil, template_image: ImageUtil, need_notice=False):
        # 生成拼图坐标点位
        self.generate_picture_points(background_image, template_image)
        # 裁剪模板图
        self.cut_by_template(background_image, template_image, self.points['x'],0)

        if need_notice:
            while True:
                newTemplateImage = self.get_template_image()
                if newTemplateImage.src != template_image.src:
                    offset_x = generate_random_int(0, background_image.width - newTemplateImage.width - 5)
                    res = float(newTemplateImage.width - offset_x) > float(newTemplateImage.width / 2)
                    if abs(res):
                        self.interference_by_template(background_image, newTemplateImage, offset_x, self.points['y'])
                        break

        return None

    def get_cache_key(self, token: str) -> str:
        return f"{self.block_puzzle_captcha_cache_key}:{token}"

    def get(self) -> dict:

        # 初始化
        background_image = self.get_background_image()
        # 设置水印
        background_image.set_text(background_image.rgba_image, self.font_water_text, self.font_water_text_font_size,
            (255, 255, 255, 255))
        # 初始化模板图片
        template_image = self.get_template_image()
        # 构造前端所需图片
        self.picture_templates_cut(background_image, template_image, need_notice=False)

        originalImageBase64 = background_image.base64_encode_image(background_image.rgba_image)
        jigsawImageBase64 = template_image.base64_encode_image(template_image.rgba_image)

        data = {
            'backgroundBase64ImageStr': self.base64_image_prefix.format(data=originalImageBase64),
            'picCheckerBase64ImageStr': self.base64_image_prefix.format(data=jigsawImageBase64),
            'token': generate_uuid(),
        }
        # 设置redis缓存
        cache_key = self.get_cache_key(data.get("token"))
        self.redis.setex(cache_key, json.dumps(self.points), self.block_puzzle_captcha_cache_key_expire)
        return data

    def check(self, token: str, point_json: dict) -> bool:

        cache_key = self.get_cache_key(token)
        cache_value_bytes = self.redis.get(cache_key)
        if not cache_value_bytes:
            return False

        cache_value = json.loads(cache_value_bytes.decode(self._data_encoding))
        # 验证位置
        diff = (
                abs(float(cache_value.get('x') - point_json.get('x'))) <=
                float(self.block_puzzle_captcha_check_offsetX)
        )
        if (
            diff and
            cache_value.get('y') == point_json.get('y')
        ):
            return True
        return False

    def verify(self, token: str, point_json: dict) -> bool:
        flag = self.check(token, point_json)
        cache_key = self.get_cache_key(token)
        if flag:
            self.redis.delete(cache_key)
            return True
        return False


if __name__ == '__main__':
    block_puzzle = BlockPuzzleCaptcha(redis_url=None)
    # print(block_puzzle.get())
    print(block_puzzle.verify("a7f3fbadefdf4b42b4ed2ca25ba222b8", {"x": 109, "y": 5}))
