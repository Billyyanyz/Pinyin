import json
from collections import Counter, defaultdict
from src.Const import accept_triple_character_bound

with open("./stats/zh_plus_pinyin_dicted_list.json", "r", encoding="UTF-8") as load_file:
    zh_plus_pinyin_dicted_list = json.load(load_file)
zh_plus_pinyin_dicted_list_all = zh_plus_pinyin_dicted_list
zh_plus_pinyin_dicted_list_all["##"] = 0
zh_plus_pinyin_dicted_list_all["$$"] = 0


def analyzer(add_to_existed = False):
    if add_to_existed:
        with open("./stats/single_character_num.json", "r", encoding="UTF-8") as load_file:
            single_character_num = Counter(json.load(load_file))
        with open("./stats/double_character_num.json", "r", encoding="UTF-8") as load_file:
            double_character_num = json.load(load_file)
        for item in double_character_num.keys():
            double_character_num[item] = Counter(double_character_num[item])
        double_character_num = defaultdict(lambda: Counter(), double_character_num)
        with open("./stats/triple_character_num.json", "r", encoding="UTF-8") as load_file:
            triple_character_num = json.load(load_file)
        for item in triple_character_num.keys():
            triple_character_num[item] = Counter(triple_character_num[item])
        triple_character_num = defaultdict(lambda: Counter(), triple_character_num)
    else:
        single_character_num = Counter()
        for item in zh_plus_pinyin_dicted_list_all.keys():
            single_character_num[item] = 0
        double_character_num = defaultdict(lambda: Counter())


    address_list = []
    with open("./original_material/mat_address_list.txt", "r", encoding="UTF-8") as load_file:
        lines = load_file.readlines()
        for line in lines:
            tmp = line[:-1].split('|')
            address_list.append(tmp[0])

    add_to_triple = []
    for address in address_list:
        print("Start analyzing file " + address + " (double character)")
        with open("./processed_material" + address, "r", encoding="UTF-8") as write_file:
            sentences = json.load(write_file)
            for sentence in sentences:
                segmented_sentence = sentence.split("|")
                prev_char = None
                for item in segmented_sentence:
                    single_character_num[item] += 1
                    if prev_char:
                        double_character_num[prev_char][item] += 1
                        if double_character_num[prev_char][item] == accept_triple_character_bound:
                            if prev_char + "|" + item not in triple_character_num:
                                add_to_triple.append(prev_char + "|" + item)
                    prev_char = item
        print("Finish analyzing file " + address + " (double character)")

    print("Start dumping analyzed file. (double character)")
    with open("./stats/single_character_num.json", "w", encoding="UTF-8") as write_file:
        json.dump(single_character_num, write_file, ensure_ascii=False)
    with open("./stats/double_character_num.json", "w", encoding="UTF-8") as write_file:
        json.dump(double_character_num, write_file, ensure_ascii=False)
    print("Finish dumping analyzed file. (double character)")

    for item in add_to_triple:
        triple_character_num[item] = Counter()
    for address in address_list:
        print("Start analyzing file " + address + " (triple character)")
        with open("./processed_material" + address, "r", encoding="UTF-8") as write_file:
            sentences = json.load(write_file)
            for sentence in sentences:
                segmented_sentence = sentence.split("|")
                prev_prev_char = None
                prev_char = None
                for item in segmented_sentence:
                    if prev_prev_char and prev_char and prev_prev_char + "|" + prev_char in triple_character_num:
                        triple_character_num[prev_prev_char + "|" + prev_char][item] += 1
                    prev_prev_char = prev_char
                    prev_char = item
        print("Finish analyzing file " + address + " (triple character)")

    print("Start dumping analyzed file. (triple character)")
    with open("./stats/triple_character_num.json", "w", encoding="UTF-8") as write_file:
        json.dump(triple_character_num, write_file, ensure_ascii=False)
    print("Finish dumping analyzed file. (triple character)")
