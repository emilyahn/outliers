import sys
import csv
import pandas as pd
import numpy as np
import random
from sklearn.covariance import MinCovDet


# Get distribution and outliers via Mahalanobis distance for vowels F1 + F2
# for Common Voice data (from formant csv files)
# ex. python src/mahal_cv.py kazakh
# ex. python src/mahal_cv.py swedish 1000

def main():
	lang_name = sys.argv[1]
	VOWEL_NUM_THRESH = 100

	# otional argument: subset to specifed # of utterances
	NUM_SUBSET = None
	if len(sys.argv) > 2:
		NUM_SUBSET = int(sys.argv[2])

	print(lang_name)
	out_file = f'data/cv8/mahal/{lang_name}_vowels_all.csv'
	# load low_spkr IDs
	low_spkr_file = f'data/cv8/{lang_name}/{lang_name}_low_spkrs.txt'
	with open(low_spkr_file, 'r') as f:
		low_spkr_list = [line.strip() for line in f.readlines()]

	# load formant file
	formant_file = f'data/cv8/{lang_name}/{lang_name}_formants_low2.csv'
	fields = ['file', 'vowel', 'prec', 'foll', 'start', 'end', 'f1_mid', 'f1_mp1', 'f1_mp2', 'f2_mid', 'f2_mp1', 'f2_mp2']
	df = pd.read_csv(formant_file, usecols=fields, encoding='utf16')

	# remove nan's
	df = df[(pd.isna(df['f1_mid']) == False)]
	df = df[(pd.isna(df['f2_mid']) == False)]
	vowel_set = set(df['vowel'])

	# filter to keep only speakers from low_spkr_list
	df = df[df['file'].str.startswith(tuple(low_spkr_list))]

	# if subsetting (i.e. Swedish) to NUM_SUBSET
	if NUM_SUBSET:
		all_utt_set = set(df['file'])
		print('total possible low utts', len(all_utt_set))
		subset_utts = random.sample(list(all_utt_set), NUM_SUBSET)
		df = df[df['file'].isin(subset_utts)]

	# average around midpoints of f1 and f2 to create new cols
	df['f1'] = df[['f1_mid', 'f1_mp1', 'f1_mp2']].mean(axis=1)
	df['f2'] = df[['f2_mid', 'f2_mp1', 'f2_mp2']].mean(axis=1)

	out_fields = ['file', 'vowel', 'prec', 'foll', 'start', 'end', 'f1', 'f2', 'MD']
	out_df = pd.DataFrame(columns=out_fields)

	for vowel in vowel_set:
		vowel_df = df.copy()
		vowel_df = vowel_df[vowel_df['vowel'] == vowel]

		# only take vowels that occur >= VOWEL_NUM_THRESH times
		if len(vowel_df) < VOWEL_NUM_THRESH:
			print(f'TOO FEW: {vowel}\t{len(vowel_df)}')
			continue

		f12 = np.stack((vowel_df['f1'], vowel_df['f2']), axis=1)
		print(vowel, len(f12))
		f12_cov = MinCovDet(random_state=0).fit(f12)

		mahal_dist_list = []
		for index in vowel_df.index:
			f1 = vowel_df['f1'][index]
			f2 = vowel_df['f2'][index]
			mahal_dist = f12_cov.mahalanobis([[f1, f2]])
			mahal_dist_list.append(mahal_dist[0])

		vowel_df['MD'] = mahal_dist_list

		out_df = out_df.append(vowel_df)

	out_df = out_df.round(3)  # 3 decimal places max
	out_df.to_csv(out_file, index=False, columns=out_fields)


if __name__ == '__main__':
	main()
