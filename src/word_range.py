import json


def word_range():
    zh_character = {}
    pinyin_zh_dict = {}
    with open("./original_material/拼音汉字表.txt", "r", encoding="GBK") as load_file:
        lines = load_file.readlines()
        for line in lines:
            if (line[-1] == '\n'):
                line = line[:-1]
            chr_list = line.split(" ")
            pinyin = chr_list[0]
            pinyin_zh_dict[pinyin] = []
            chr_list.pop(0)
            for item in chr_list:
                zh_character[item + pinyin] = 0
                pinyin_zh_dict[pinyin].append(item)

    with open("../src/stats/zh_plus_pinyin_dicted_list.json", "w", encoding="UTF-8") as write_file:
        json.dump(zh_character, write_file, ensure_ascii=False)

    with open("../src/stats/pinyin_to_zh_dict.json", "w", encoding="UTF-8") as write_file:
        json.dump(pinyin_zh_dict, write_file, ensure_ascii=False)

    print("Chinese and pinyin lists and dictionaries initialized.")
