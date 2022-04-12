import sys
import csv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict
from scipy.stats import norm


# Get distribution and outliers via Mahalanobis distance for vowels F1 + F2
# for Common Voice data (from formant csv files)

def main():
	lang_name = sys.argv[1]
	print(lang_name)
	# load low_spkr IDs
	# low_spkr_file = f'data/cv8/{lang_name}/{lang_name}_low_spkrs.txt'
	# with open(low_spkr_file, 'r') as f:
	# 	low_spkr_list = [line.strip() for line in f.readlines()]

	# load formant file
	formant_file = f'data/cv8/{lang_name}/{lang_name}_formants_low2_head5.csv'
	fields = ['file', 'vowel', 'prec', 'foll', 'start', 'end', 'f1_mid', 'f1_mp1', 'f1_mp2', 'f2_mid', 'f2_mp1', 'f2_mp2']
	df = pd.read_csv(formant_file, usecols=fields, encoding='utf16')

	df['f1'] = df[['f1_mid', 'f1_mp1', 'f1_mp2']].mean(axis=1)
	df['f2'] = df[['f2_mid', 'f2_mp1', 'f2_mp2']].mean(axis=1)
	#TODO: filter to keep only speakers from low_spkr_list


if __name__ == '__main__':
	main()
