# -*- coding:utf-8 -*-
import json
import base64
import requests
import glob
import time

url = 'http://192.168.13.212:8012/pc/ocr'

def post_method(image_str):
    headers = {'content-type': 'application/json'}
    request_data = {'key': '123',
                    'image':image_str}
    ret = requests.post(url, json=request_data, headers=headers)
    if ret.status_code == 200:
        result = ret.text
        print('result:{}'.format(result))
        return result
    return ''        

if __name__ == '__main__':
    files = glob.glob('/Users/pconline/Documents/ocr_image/*png')
    log_file = open('/Users/pconline/Documents/ocr_image/202005131357.txt','w',encoding='utf-8')
    i = 0
    for file in files:
        if i > 0:
            break
        f = open(file,'rb')
        base64data = base64.b64encode(f.read())
        image = str(base64data, 'utf-8')
        print("file:{}, len:{}".format(file.split('/')[-1],len(image)))
        res = post_method(image)
        log_file.write(file + '\n')
        log_file.write(res)
        log_file.write('\n------------------------------------------------------\n')
        i += 1


            




