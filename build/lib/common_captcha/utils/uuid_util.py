#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid


def generate_uuid() -> str:
    """
    generate uuid string
    :return: str
    """

    return uuid.uuid4().hex
