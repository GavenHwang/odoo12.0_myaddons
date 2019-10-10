# -*- coding: utf-8 -*-

from core.patch.database import patch_database


def monkey_patch():
    patch_database()
