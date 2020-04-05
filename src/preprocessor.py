import json
import os
from pypinyin import lazy_pinyin

with open("./stats/zh_plus_pinyin_dicted_list.json", "r", encoding="UTF-8") as load_file:
    zh_plus_pinyin_dicted_list = json.load(load_file)
zh_plus_pinyin_dicted_list_all = zh_plus_pinyin_dicted_list
zh_plus_pinyin_dicted_list_all["##"] = 0
zh_plus_pinyin_dicted_list_all["$$"] = 0

backup_zh_dict = {}
for item in zh_plus_pinyin_dicted_list_all.keys():
    backup_zh_dict[item[0]] = item[1:]


def get_sentences(content):
    sentences = []
    current_sentence = "#"
    for char in content:
        if '\u4e00' <= char <= '\u9fff':
            if char not in backup_zh_dict:
                if len(current_sentence) > 0 and current_sentence != "#":
                    sentences.append(current_sentence)
                current_sentence = ""
            else:
                current_sentence += char
        else:
            if len(current_sentence) > 0 and current_sentence != "#":
                if not char.encode("UTF-8").isalnum():
                    current_sentence += "$"
                sentences.append(current_sentence)
            current_sentence = ""
            if not char.encode("UTF-8").isalnum():
                current_sentence += "#"
    if len(current_sentence) > 0 and current_sentence != "#":
        sentences.append(current_sentence)
    return sentences


def process(material, mat_style):
    sentences = []
    lines = material.readlines()
    if mat_style == "0":
        for line in lines:
            sentences += get_sentences(line)
    elif mat_style == "1":
        for line in lines:
            try:
                content = json.loads(line)["html"]
            except:
                continue
            if content[0:3] == "原标题":
                content = content[4:]
            sentences += get_sentences(content)
    elif mat_style == "2":
        for line in lines:
            if line == "\n" or (len(line) > 4 and (line[0:4] == "消息分组" or line[0:4] == "消息记录"
                                                   or line[0:4] == "====" or line[0:4] == "[图片]" or line[0:4] == "[表情]"
                                                   or (line[0:2] == "20" and line[4] == "-"))):
                continue
            sentences += get_sentences(line)
    return sentences


def add_pinyin(sentences):
    pinyined_sentences = []
    for sentence in sentences:
        pinyin_of_sentence = lazy_pinyin(sentence)
        pinyined_sentence = ""
        for i in range(len(sentence)):
            item = sentence[i] + pinyin_of_sentence[i]
            if item not in zh_plus_pinyin_dicted_list_all:
                item = sentence[i] + backup_zh_dict[sentence[i]]
            pinyined_sentence += item + "|"
        pinyined_sentences.append(pinyined_sentence[:-1])
    return pinyined_sentences


def preprocessor(add_new_materials = True):
    address_list = []
    with open("./original_material/mat_address_list.txt", "r", encoding="UTF-8") as load_file:
        lines = load_file.readlines()
        for line in lines:
            tmp = line.split('|')
            address_list.append([tmp[0], tmp[1], tmp[2]])

    for address in address_list:
        if not (add_new_materials and os.path.isfile("./processed_material" + address[0])):
            with open("./original_material" + address[0], "r", encoding=address[2], errors="ignore") as material:
                print("Start preprocessing file " + address[0])
                processed_material = process(material, address[1])
                processed_material = add_pinyin(processed_material)
                with open("./processed_material" + address[0], "w", encoding="UTF-8") as write_file:
                    json.dump(processed_material, write_file, ensure_ascii=False)
                print("Finish preprocessing file " + address[0])
