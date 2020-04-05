import sys
import os

os.chdir("./src/")
from src import word_range, preprocessor, analyzer, num_to_freq_translater

if __name__ == "__main__":
	if len(sys.argv) == 1 or len(sys.argv) >= 3:
		print("Usage:\n  pinyin <command> [arguments]")
		print("Command:")
		print("  run_all              run through the whole preparation from scratch (require address list)")
		print("  process              process and analyze original materials and cover existed stats(require address list)")
		print("  add_new              add new materials to the existed stats(require address list)")
		print("  reanalyze            reanalyze existing materials (if triple_character_bound modified)")
		print("  translate            interpret stats into possibility matrices (if zero_possibility_bound modified)")
	elif len(sys.argv) == 2:

		if sys.argv[1] == "run_all":
			word_range.word_range()
			preprocessor.preprocessor(False)
			analyzer.analyzer(False)
			num_to_freq_translater.num_to_freq_translater()
		elif sys.argv[1] == "process":
			preprocessor.preprocessor(False)
			analyzer.analyzer(False)
			num_to_freq_translater.num_to_freq_translater()
		elif sys.argv[1] == "add_new":
			preprocessor.preprocessor(True)
			analyzer.analyzer(True)
			num_to_freq_translater.num_to_freq_translater()
		elif sys.argv[1] == "reanalyze":
			analyzer.analyzer(False)
			num_to_freq_translater.num_to_freq_translater()
		elif sys.argv[1] == "translate":
			num_to_freq_translater.num_to_freq_translater()
		else:
			print("Illegal command")
