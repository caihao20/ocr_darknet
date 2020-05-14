# -*- coding: utf-8 -*-
import os
import jieba
import csv
import jieba.posseg as pseg
import jieba.analyse
import re
import pickle
import time

class ExtractEntity(object):
    """docstring for extract_entity"""
    def __init__(self):
        super(ExtractEntity, self).__init__()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DATA_PATH = BASE_DIR + '/service/data/'
        self.flags_extract = ['BRAND', 'SERIES', 'FACTORY']
        self.pkl_path = self.DATA_PATH + 'pkl/'

        
        self.stopwords_list = self.get_stopword_list()
        self.add_user_dict()

    def add_user_dict(self):
        jieba.re_han_default = re.compile('([\u4E00-\u9FD5a-zA-Z0-9+#&\._% -]+)', re.U)

        id_name_brand = pickle.load(open(self.pkl_path + 'entity_id_brand.pkl','rb'))
        for key,value in dict(id_name_brand).items():
            jieba.add_word(key,  tag='BRAND')

        id_name_factory = pickle.load(open(self.pkl_path + 'entity_id_factory.pkl','rb'))
        for key,value in dict(id_name_factory).items():
            jieba.add_word(key, tag='FACTORY')

        id_name_series = pickle.load(open(self.pkl_path + 'entity_id_series.pkl','rb'))
        for key,value in dict(id_name_series).items():
            jieba.add_word(key, tag='SERIES')

        jieba.add_word('续航里程', freq=999999, tag='CONF_ITEM')
        jieba.add_word('ESP', freq=999999, tag='OO')


    def get_stopword_list(self): 
        PATH_STOPWORDS = self.DATA_PATH + 'stopwords_cn.txt'
        stopword_list = [sw.replace('\n', '') for sw in open(PATH_STOPWORDS, encoding='utf-8').readlines()]
        return stopword_list


    def cut_sentence(self, sentence):
        # sentence = re.sub("[，。？！、,]", "", sentence)
        seg_list = pseg.lcut(sentence)
        seg_list = [i for i in seg_list if i.word not in self.stopwords_list]
        filtered_words_list = set()
        word_flag = dict()

        last_flag = ''
        last_word = ''
        w_flag = ''
        for seg in seg_list:
            if seg.flag in self.flags_extract:
                if last_flag and last_word:
                    word_flag[last_word.strip()] = last_flag
                    filtered_words_list.add(last_word.strip())
                if last_word and (last_word in seg.word or last_flag == 'SERIES'):
                    last_word = seg.word
                else:
                    last_word = last_word + seg.word

                last_flag = seg.flag
                w_flag = seg.flag     
            elif seg.flag in ["x", "eng"] and last_word: # "m"可以表示车型关键词
                if last_flag in ['BRAND', 'FACTORY']:
                    w_flag = 'SERIES'
                last_flag = seg.flag
                last_word = last_word + seg.word           
            else:
                if last_word and len(last_word.replace(' ', '')) > 1 \
                    and not re.findall('[0-9]+km', last_word):
                    filtered_words_list.add(last_word.strip())
                    word_flag[last_word.strip()] = w_flag
                last_flag = ''
                last_word = ''
                w_flag = ''

        if last_word and len(last_word.replace(' ', '')) > 1 \
            and not re.findall('[0-9]+km', last_word):
            filtered_words_list.add(last_word.strip())
            word_flag[last_word.strip()] = w_flag       
                                                              

        return filtered_words_list, word_flag     
    
    def extract_result(self, sentence):
        filtered_words_list, word_flag = self.cut_sentence(sentence)
        return list(filtered_words_list)

    def extract_result_flag(self, sentence):
        filtered_words_list, word_flag = self.cut_sentence(sentence)
        return word_flag

    def extract_result_json(self, sentence):
        entity_id_brand = pickle.load(open(self.pkl_path + 'entity_id_brand.pkl','rb'))
        entity_id_series = pickle.load(open(self.pkl_path + 'entity_id_series.pkl','rb'))
        entity_id_factory = pickle.load(open(self.pkl_path + 'entity_id_factory.pkl','rb'))
        # print('extract_result：{}'.format(sentence))
        filtered_words_list, word_flag = self.cut_sentence(sentence)

        list_brand = list()
        list_series = list()
        list_factory = list()

        # print(word_flag)

        for key, value in word_flag.items():
            if value == 'BRAND':
                b_id = entity_id_brand.get(key, '')
                if b_id:
                    list_brand.append({key: str(b_id)})
            elif value == 'FACTORY':
                b_id = entity_id_factory.get(key, '')
                if b_id:
                    list_factory.append({key: str(b_id)})
            elif value == 'SERIES':
                b_id = entity_id_series.get(key, '')
                if b_id == '':
                    if not re.search('[\u4e00-\u9fa5]+', key):
                        continue                       
                list_series.append({key: str(b_id)})

        results = dict()
        results['brand'] = list_brand
        results['factory'] = list_factory
        results['series'] = list_series

        return results       



# if __name__ == '__main__':

#     # 14677863, 14721255, 14742475, 14744755, 14761596,14783775
#     f_content = open('data/article/14783775.txt','r',encoding='utf-8').read().replace('\n','')
#     # f_content = get_entity_by_reg(f_content)
#     # print(f_content)
#     # f_content = re.sub(r'\d','',f_content)

#     extract_entity = ExtractEntity()
#     sentence_cuted, flag_dict = extract_entity.cut_sentence(f_content)
#     print(sentence_cuted)
#     print(flag_dict)














































