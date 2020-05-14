#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config
@author: chineseocr
"""
import os
current_dir = os.path.dirname(__file__)


ocrType = 'chinese'
ocrPath  = os.path.join(current_dir, 'models/ocr/{}/ocr.weights'.format(ocrType))
textPath = os.path.join(current_dir, 'models/text/text.weights')
darkRoot =os.path.join(current_dir, 'darknet/libdarknet.so') ##darknet 
TEXT_LINE_SCORE=0.7##text line prob
scale = 800##可动态修改 no care text.cfg height,width
maxScale = 1000
GPU=True #False ## gpu for darknet  or cpu for opencv.dnn 
anchors = '16,11, 16,16, 16,23, 16,33, 16,48, 16,68, 16,97, 16,139, 16,198, 16,283'
