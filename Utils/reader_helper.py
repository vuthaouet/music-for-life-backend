# coding: utf-8

import json
import codecs

def load_json(file_path):
    data = json.load(codecs.open(file_path, 'r', 'utf-8-sig'))
    return data


# print(load_json("/media/kodiak/New Volume/Ky_II_2019_2020/PTUDDD/mindBook_backend"))