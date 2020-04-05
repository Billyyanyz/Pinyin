from pathlib import Path
from src import HMM_pinyin


def run_main():
	with open(Path(__file__).parent / "./data/input.txt") as load_file:
		lines = load_file.readlines()
		pinyin_lists = []
		for line in lines:
			if line[-1] == "\n":
				line = line[:-1]
			pinyin_lists.append(line.split(" "))
		answer_lists = HMM_pinyin.HMM(pinyin_lists)
	output_lists = []
	for answer in answer_lists:
		answer_str = ""
		for item in answer:
			answer_str += item
		output_lists.append(answer_str)
	with open(Path(__file__).parent / "./data/output.txt", "w", encoding="UTF-8") as write_file:
		for item in output_lists:
			write_file.write(item + "\n")


if __name__ == "__main__":
	run_main()