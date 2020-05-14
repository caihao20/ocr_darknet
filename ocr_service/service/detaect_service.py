# -*- coding: utf-8 -*-

import tensorflow as tf

from django.conf import settings



def get_session():
    sess_list = settings.PARAM["sess"]
    nbr_gpus = settings.PARAM["gpus"]
    index = random.randint(0, 10) % nbr_gpus
    return sess_list[index]


def predict_img(self, img):
    height = img.height
    width = img.width
    scale = height / width

    print('height:{},width:{},scale:{},'.format(height,width,scale))

    results = []
    t = time.time()
    if scale > 1.5 and height > 2560:
        # todo 重叠部分系数(coefficient) = width/10
        coe = 0.1
        height_s = width * (1 - coe)
        for i in range(int(height / height_s + 1)):
            height_y = i * height_s
            pt1 = (0, min(height_y, height - width))
            pt3 = (width , min(height_y + width, height))
            img_crop = img.crop((pt1[0], pt1[1], pt3[0], pt3[1]))

            text_recs_all, text_recs_len, img_all = predict_quad(self.east_model, img_crop)
            print("Mission complete, it took {:.3f}s".format(time.time() - t))
            print("result ：box:{}".format(text_recs_all[s]))
            results = text_recs_all

    else:
        text_recs_all, text_recs_len, img_all = predict_quad(self.east_model, img)
        print('text_recs_all:{}'.format(text_recs_all))
        print("Mission complete, it took {:.3f}s".format(time.time() - t))
        results = text_recs_all

    return results

def rect_point(box):
    x1 = min(box[0], box[4])
    x2 = max(box[2], box[6])
    y1 = min(box[1], box[3])
    y2 = max(box[5], box[7])
    w = x2 - x1
    h = y2 - y1

    return [x1, y1, w, h]    


def detect_result(base64Image):    
    base64Image = base64Image.encode('utf-8')
    img_base64 = base64.b64decode(base64Image)
    img = Image.open(io.BytesIO(img_base64)).convert('RGB')
    # w,h = img.size
    # image = np.array(img.convert('RGB'))

    results = []

    pre_results = predict_img(img)

    for rect in pre_results:
        rect = [int(i) for i in rect]
        results.append({'box': rect_point(rect), 'text': '' })
    
    return results



