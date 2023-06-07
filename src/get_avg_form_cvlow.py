import sys
import csv
import os
import numpy as np
import pandas as pd
from collections import defaultdict
from statistics import mean
from scipy.stats import norm


# for 1 Common Voice lang, get AVG F1/F2 per vowel per speaker
# outfile format: spkr_id, vowel, F1 avg, F2 avg, V_count_spkr
# to run:
# python get_avg_form_cvlow.py {lang} {narrow|broad} {filter|no_filter}
# ex:
# python src/get_avg_form_cvlow.py hausa narrow filter > data/cv8/formants/hausa_avg_formants_narrow_filter.tsv

lang = sys.argv[1]
narrow_broad = sys.argv[2]  # 'narrow' or 'broad'
filter_out = sys.argv[3]  # 'filter' or 'no_filter'

if filter_out == 'filter':
	filter_out = True
else:
	filter_out = False

is_swedish = False
if lang == 'swedish':
	is_swedish = True

# load low formant files
low_formant_infile = f'data/cv8/{lang}/{lang}_formants_low2.csv'

if is_swedish:
	# load formant file
	subset_formant_file = f'data/cv8/mahal/swedish_vowels_all.csv'
	fields = ['file']
	# df = pd.read_csv(subset_formant_file, usecols=fields, encoding='utf16')
	df = pd.read_csv(subset_formant_file, usecols=fields)
	swedish_file_set = set(df['file'])
	# print(len(swedish_file_set), file=sys.stderr)
	# print(swedish_file_set, file=sys.stderr)

def process_vowel(raw_vowel, nar_bro):
	vowel = raw_vowel
	if nar_bro == 'narrow':
		if len(raw_vowel) > 1:
			# keep the following 2nd symbols
			if raw_vowel[1] in ['ː', '̃', 'o', 'e', 'ɤ']:
				vowel = raw_vowel[:2]
			else:
				vowel = raw_vowel[0]

			# maltese case, keep e.g. 'ɪˤː'
			if len(raw_vowel) > 2:
				if raw_vowel[2] == 'ː':
					vowel = raw_vowel[:3]

	elif nar_bro == 'broad':
		if len(raw_vowel) > 1:
			# keep the following 2nd symbols
			if raw_vowel[1] in ['o', 'e', 'ɤ']:
				vowel = raw_vowel[:2]
			else:
				vowel = raw_vowel[0]

	return vowel


def process_vowel_dict(formant_infile, setting):
	# spkr_list = setting_dict[setting]
	spkr_vowel_dict = {}  # spkr_vowel_dict[spkr][vowel] = list(tuples(f1,f2))
	vowel_ft_dict = {}  # vowel_ft_dict[vowel][{'f1','f2'}] = list(float)
	# skip_dur = 0
	try:
		with open(formant_infile, encoding='utf-16') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')

			for row in reader:

				if is_swedish:
					if row['file'] not in swedish_file_set:
						continue

				spkr = row['file'].split('_')[0]  # ex. 00004
				# if spkr not in spkr_list:
				# 	continue

				if filter_out:
					if float(row['dur']) > 0.3:
						# skip_dur += 1
						continue

				raw_vowel = row['vowel']
				vowel = process_vowel(raw_vowel, narrow_broad)

				f1 = mean([float(row['f1_mid']), float(row['f1_mp1']), float(row['f1_mp2'])])
				f2 = mean([float(row['f2_mid']), float(row['f2_mp1']), float(row['f2_mp2'])])

				if spkr not in spkr_vowel_dict:
					spkr_vowel_dict[spkr] = defaultdict(list)

				if vowel not in vowel_ft_dict:
					vowel_ft_dict[vowel] = defaultdict(list)

				spkr_vowel_dict[spkr][vowel].append((f1, f2))  # tuple
				vowel_ft_dict[vowel]['f1'].append(f1)
				vowel_ft_dict[vowel]['f2'].append(f2)

	except:
		# remove encoding
		with open(formant_infile) as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',')

			for row in reader:

				if is_swedish:
					if row['file'] not in swedish_file_set:
						continue

				spkr = row['file'].split('_')[0]  # ex. 00004

				# if spkr not in spkr_list:
				# 	continue

				if filter_out:
					if float(row['dur']) > 0.3:
						# skip_dur += 1
						continue

				raw_vowel = row['vowel']
				vowel = process_vowel(raw_vowel, narrow_broad)

				f1 = mean([float(row['f1_mid']), float(row['f1_mp1']), float(row['f1_mp2'])])
				f2 = mean([float(row['f2_mid']), float(row['f2_mp1']), float(row['f2_mp2'])])

				if spkr not in spkr_vowel_dict:
					spkr_vowel_dict[spkr] = defaultdict(list)

				if vowel not in vowel_ft_dict:
					vowel_ft_dict[vowel] = defaultdict(list)

				spkr_vowel_dict[spkr][vowel].append((f1, f2))  # tuple
				vowel_ft_dict[vowel]['f1'].append(f1)
				vowel_ft_dict[vowel]['f2'].append(f2)

	# process vowel_ft_dict first, save thresholds (2SD away from mean)
	thresh_dict = defaultdict(dict)  # thresh_dict[vowel][{'f1','f2'}] = (float, float)
	for vowel in vowel_ft_dict:
		for ft in vowel_ft_dict[vowel]:  # iterate over ['f1', 'f2']
			mu, std = norm.fit(vowel_ft_dict[vowel][ft])
			lower_thresh = mu - (2 * std)
			upper_thresh = mu + (2 * std)
			thresh_dict[vowel][ft] = (lower_thresh, upper_thresh)

	# skip_thresh = 0
	# then get avgs per speaker, filtering out > 2SD, print
	for spkr in spkr_vowel_dict:
		for vowel, form_list in spkr_vowel_dict[spkr].items():
			f1_keep_list = []
			f2_keep_list = []
			for tup in form_list:
				# skip if any of F1 or F2 is out of bounds
				if filter_out:
					if tup[0] < thresh_dict[vowel]['f1'][0] or tup[0] > thresh_dict[vowel]['f1'][1] or tup[1] < thresh_dict[vowel]['f2'][0] or tup[1] > thresh_dict[vowel]['f2'][1]:
						# skip_thresh += 1
						# print(vowel, tup, thresh_dict[vowel]['f1'], thresh_dict[vowel]['f2'])
						continue

				f1_keep_list.append(tup[0])
				f2_keep_list.append(tup[1])

			# list may be empty. then don't print
			if not f1_keep_list:
				continue

			mean_f1 = mean(f1_keep_list)
			mean_f2 = mean(f2_keep_list)

			print(f'{spkr}\t{vowel}\t{mean_f1:.2f}\t{mean_f2:.2f}\t{len(f1_keep_list)}')

	# print("DUR SKIP", file=sys.stderr)
	# print(skip_dur, file=sys.stderr)
	# print("THRESH SKIP", file=sys.stderr)
	# print(skip_thresh, file=sys.stderr)

print('spkr\tvowel\tmean_f1\tmean_f2\tV_count_spkr')
process_vowel_dict(low_formant_infile, 'low')
# process_vowel_dict(high_formant_infile, 'high')
