import json
from pathlib import Path
from src.Const import triple_transfer_weight, double_transfer_weight, zero_possibility_bound


print("Start initialization.")
with open(Path(__file__).parent / "./stats/single_character_freq.json", "r", encoding="UTF-8") as load_file:
	single_character_freq = json.load(load_file)
with open(Path(__file__).parent / "./stats/double_character_freq.json", "r", encoding="UTF-8") as load_file:
	double_character_freq = json.load(load_file)
with open(Path(__file__).parent / "./stats/triple_character_freq.json", "r", encoding="UTF-8") as load_file:
	triple_character_freq = json.load(load_file)
with open(Path(__file__).parent / "./stats/pinyin_to_zh_dict.json", "r", encoding="UTF-8") as load_file:
	pinyin_to_zh_dict = json.load(load_file)
pinyin_to_zh_dict["#"] = ["#"]
pinyin_to_zh_dict["$"] = ["$"]
print("Finish initialization.")


def transfer_2(prev_item, item):
	res = double_transfer_weight * double_character_freq.get(prev_item, dict()).get(item, zero_possibility_bound) + \
	      (1 - double_transfer_weight) * single_character_freq.get(item, zero_possibility_bound)
	return res


def transfer(prev_prev_item, prev_item, item):
	res = triple_transfer_weight * triple_character_freq.get(prev_prev_item + "|" + prev_item, dict()).get(item, zero_possibility_bound) + \
	      (1 - triple_transfer_weight) * double_transfer_weight *double_character_freq.get(prev_item, dict()).get(item, zero_possibility_bound) + \
	      (1 - triple_transfer_weight) * (1 - double_transfer_weight) * single_character_freq.get(item, zero_possibility_bound)
	return res


def HMM(pinyin_lists):
	result_lists = []
	for pinyin_list in pinyin_lists:
		pinyin_list = ["#"] + pinyin_list + ["$"]
		l = len(pinyin_list)
		max_p = {}
		for i in range(l):
			max_p[i] = {}
		max_p[0]["#"] = (0, None)
		for zh in pinyin_to_zh_dict[pinyin_list[1]]:
			max_p[1][zh] = {}
			max_p[1][zh]["#"] = (max_p[0]["#"][0] + transfer_2("##", zh + pinyin_list[1]), "##")
		for i in range(2, l):
			for zh in pinyin_to_zh_dict[pinyin_list[i]]:
				max_p[i][zh] = {}
				for prev_zh in pinyin_to_zh_dict[pinyin_list[i - 1]]:
					max = -l * 1000.0
					max_zh = None
					for prev_prev_zh in pinyin_to_zh_dict[pinyin_list[i - 2]]:
						tmp = max_p[i - 1][prev_zh][prev_prev_zh][0] + \
						      transfer(prev_prev_zh + pinyin_list[i - 2], prev_zh + pinyin_list[i - 1], zh + pinyin_list[i])
						if tmp > max:
							max = tmp
							max_zh = prev_prev_zh
					max_p[i][zh][prev_zh] = (max, max_zh)
		result_list = []
		for i in range(l):
			result_list.append("$")
		total_max = -l * 1000.0
		for zh in pinyin_to_zh_dict[pinyin_list[l - 2]]:
			if max_p[l - 1]["$"][zh][0] > total_max:
				total_max = max_p[l - 1]["$"][zh][0]
				result_list[l - 2] = zh
		for i in range(l - 3, -1, -1):
			result_list[i] = max_p[i + 2][result_list[i + 2]][result_list[i + 1]][1]
		result_list = result_list[1:-1]
		result_lists.append(result_list)
	return result_lists
