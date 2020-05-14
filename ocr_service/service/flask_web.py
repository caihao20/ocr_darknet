# -*- coding: utf-8 -*-
import os
import json

from flask import Flask
from flask import request
from flask import jsonify

import ocr_service.service.ocr_tag as eej
from ocr_service.service.pc_extract_entity import ExtractEntity
extract_ent = ExtractEntity()

app = Flask(__name__)

def test():
    import base64     
    
    test_img = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            'service/darknet_ocr/test/test3.jpg')
    imgString = str(base64.b64encode(open(test_img,'rb').read()), encoding='utf-8')
    result = eej.ocr_result(imgString)
    print('test:{}, result: {}'.format(test_img,result))

test()    


@app.route('/pc/ocr', methods=['POST', 'GET'])
def ocr_ent():
    result = {}
    image = ''
    request_type = ''
    image = request.args.get('image', '')
    # result['key'] = request.POST.get('key', '')
    request_type = request.POST.get('otype', '')
    content = request.POST.get('text', '')

    if not image and not text:
        result["code"] = 1
        result["err_message"] = "image or text is none"
    else:    
        if request_type == 'text':
            res = extract_ent.extract_result_json(content)
        elif request_type == 'image':
            
            res, cnt = eej.ocr_result(image)
            # result['content'] = cnt
            
        result["entity"] = res
        result["code"] = 0

    # dumps = json.dumps(result, ensure_ascii=False)
    # print('result: {}'.format(result))
    return jsonify(result)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=8013)    































