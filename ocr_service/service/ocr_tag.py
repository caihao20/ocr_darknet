# -*- coding: utf-8 -*-
import os, sys
import numpy as np
from PIL import Image
import io
import base64

import ocr_service.service.darknet_ocr.config
from ocr_service.service.darknet_ocr.text_recognize import recog_text
from ocr_service.settings import extract_ent
import json

def ocr_result(img_str):
    res = recog_text(None, img_str)
    # print(res)
    json_res = res #json.loads(res)
    errCode = json_res['errCode']
    content = ''
    if errCode <= 1:
        for d in json_res['data']:
            content += d['text']
    # content = sub_str(content)
    ext_result =  extract_ent.extract_result_json(content)
    return ext_result, content

import re
pattern = re.compile(r'[^a-zA-Z0-9\u4e00-\u9fa5]')
def sub_str(text):
    return re.sub(pattern, '', text) #.decode('utf-8')
















