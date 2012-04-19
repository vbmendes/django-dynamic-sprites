# -*- coding: utf-8 -*-

import re
import unidecode


def slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+', '-', str)
