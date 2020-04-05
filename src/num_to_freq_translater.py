import json
from math import log
from src.Const import zero_possibility_bound


def num_to_freq_translater():
    print("Start translating analysis.")

    with open("./stats/single_character_num.json", "r", encoding="UTF-8") as load_file:
        single_character_num = json.load(load_file)
    with open("./stats/double_character_num.json", "r", encoding="UTF-8") as load_file:
        double_character_num = json.load(load_file)
    with open("./stats/triple_character_num.json", "r", encoding="UTF-8") as load_file:
        triple_character_num = json.load(load_file)

    single_character_freq = {}
    single_character_sum = sum(single_character_num.values())
    for item in single_character_num.keys():
        if single_character_num[item] == 0:
            single_character_freq[item] = zero_possibility_bound
        else:
            single_character_freq[item] = log(single_character_num[item] / single_character_sum)

    double_character_freq = {}
    for item in double_character_num.keys():
        double_character_freq[item] = {}
        double_character_sum = sum(double_character_num[item].values())
        for next_item in double_character_num[item].keys():
            double_character_freq[item][next_item] = log(
                double_character_num[item][next_item] / double_character_sum)

    triple_character_freq = {}
    for item in triple_character_num.keys():
        triple_character_freq[item] = {}
        triple_character_sum = sum(triple_character_num[item].values())
        for next_next_item in triple_character_num[item].keys():
            triple_character_freq[item][next_next_item] = log(
                triple_character_num[item][next_next_item] / triple_character_sum)

    with open("./stats/single_character_freq.json", "w", encoding="UTF-8") as write_file:
        json.dump(single_character_freq, write_file, ensure_ascii=False)
    with open("./stats/double_character_freq.json", "w", encoding="UTF-8") as write_file:
        json.dump(double_character_freq, write_file, ensure_ascii=False)
    with open("./stats/triple_character_freq.json", "w", encoding="UTF-8") as write_file:
        json.dump(triple_character_freq, write_file, ensure_ascii=False)

    print("Finish translating analysis.")
