#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random


def generate_random_int(min_value: int, max_value: int) -> int:
    """
    generate random int number
    :param min_value:
    :param max_value:
    :return: int
    """

    if (min_value >= max_value) or max_value == 0:
        return max_value
    random.seed(time.time())
    return random.randint(min_value, max_value)


def generate_code(code_length: int = 6) -> str:
    """ 生成随机的code_length位数的验证码 """

    code = ''
    for i in range(code_length):
        n = random.randint(0, 9)
        b = chr(random.randint(65, 90))
        c = chr(random.randint(97, 122))
        code += str(random.choice([n, b, c]))
    return code


def generate_code_chr() -> str:
    """ 获取一个随机字符, 数字或小写字母 """
    random_num = str(random.randint(0, 9))
    random_low_alpha = chr(random.randint(97, 122))
    random_char = random.choice([random_num, random_low_alpha])
    return random_char


def generate_random_background_color() -> tuple:
    """ 生成随机的背景 """

    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return c1, c2, c3
