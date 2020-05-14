# -*- coding: utf-8 -*-
import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import ocr_service.service.ocr_tag as eej
from ocr_service.settings import extract_ent


def test():
    import base64     
    
    test_img = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            'service/darknet_ocr/test/test3.jpg')
    imgString = str(base64.b64encode(open(test_img,'rb').read()), encoding='utf-8')
    result = eej.ocr_result(imgString)
    print('test:{}, result: {}'.format(test_img,result))

# test()    

@csrf_exempt
def postmethod(request):
    result = {}
    image = ''
    request_type = ''
    if request.method == 'POST':
        image = request.POST.get('image', '')
        result['key'] = request.POST.get('key', '')
        request_type = request.POST.get('otype', '')
        content = request.POST.get('text', '')

    if not image and not content:
        result["code"] = 1
        result["err_message"] = "image or text is none"
    else:    
        if request_type == 'text':
            res = extract_ent.extract_result_json(content)
        elif request_type == 'image':
            res, cnt = eej.ocr_result(image)
            result['content'] = cnt
            
        result["entity"] = res
        result["code"] = 0

    dumps = json.dumps(result, ensure_ascii=False)
    # print('result: {}'.format(result))    

    return HttpResponse(dumps,content_type='application/json', charset='utf-8') 
    # JsonResponse(data, json_dumps_params={'ensure_ascii':False})                   