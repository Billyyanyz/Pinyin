from pathlib import Path
from src.HMM_pinyin import HMM


def tester():
    with open(Path(__file__).parent / "./data/test.txt", "r", encoding="UTF-8") as load_file:
        lines = load_file.readlines()
        pinyin = lines[::2]
        standard_answer_list = lines[1::2]
        pinyin_lists = []
        for i in range(len(pinyin)):
            pinyin_lists.append(pinyin[i][:-1].lower().split(" "))
        for i in range(len(standard_answer_list)):
            standard_answer_list[i] = standard_answer_list[i][:-1]
        answer_lists = HMM(pinyin_lists)

    real_answer_list = []
    for answer in answer_lists:
        answer_str = ""
        for item in answer:
            answer_str += item
        real_answer_list.append(answer_str)

    with open(Path(__file__).parent / "./data/standard.txt", "w", encoding="UTF-8") as write_file:
        for item in standard_answer_list:
            write_file.write(item + "\n")
    with open(Path(__file__).parent / "./data/answer.txt", "w", encoding="UTF-8") as write_file:
        for item in real_answer_list:
            write_file.write(item + "\n")

    character_accuracy = [0, 0]
    sentence_accuracy = [0, 0]
    for i in range(len(standard_answer_list)):
        sentence_accuracy[1] += 1
        correct = True
        for j in range(len(standard_answer_list[i])):
            character_accuracy[1] += 1
            if j < len(real_answer_list[i]) and standard_answer_list[i][j] == real_answer_list[i][j]:
                character_accuracy[0] += 1
            else:
                correct = False
        if correct:
            sentence_accuracy[0] += 1

    with open(Path(__file__).parent / "./data/result.txt", "w", encoding="UTF-8") as write_file:
        write_file.write(
            "character accuracy is " + str(character_accuracy[0]) + "/" + str(character_accuracy[1]) + "\n")
        write_file.write("sentence accuracy is " + str(sentence_accuracy[0]) + "/" + str(sentence_accuracy[1]) + "\n")

if __name__ == "__main__":
    tester()