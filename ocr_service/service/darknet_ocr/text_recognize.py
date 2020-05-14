# -*- coding: utf-8 -*-

import os, sys
current_path = os.path.abspath(os.path.dirname(__file__))
print(current_path)
root_path = os.path.split(current_path)[0]
sys.path.append(root_path)
sys.path.append(os.path.dirname(__file__))

print(sys.path)
import uuid
import json
import cv2
import numpy as np
from helper.image import read_url_img,base64_to_PIL,get_now
from dnn.main import text_ocr
from config import scale,maxScale,TEXT_LINE_SCORE

billList =[]
root = './test/'
timeOutTime=5

def job(uid,url,imgString):
    now = get_now()
    if url is not None:
        img=read_url_img(url)
    elif imgString is not None:
        img= base64_to_PIL(imgString)
    else:
        img = None
        
    if img is not None:
        image = np.array(img)
        image =  cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        data = text_ocr(image,scale,maxScale,TEXT_LINE_SCORE)
        
        res = {'data':data,'errCode':0}
    else:
        res = {'data':[],'errCode':3}
    return res

def recog_text(url, imgString):
    post = {"errCode":0,"errMess":""}
    uid = uuid.uuid1().__str__()
    if url is None and imgString is None:
        post["errCode"]=2
    else:
        post["errCode"] = 1
        res = job(uid, url, imgString)
        post.update(res)

    return post
    # return json.dumps(post,ensure_ascii=False)                        

  
if __name__ == "__main__":
    import base64     

    imgString = str(base64.b64encode(open('test/test3.jpg','rb').read()), encoding='utf-8')      

    res = recog_text(None, imgString)
    print(res)
      
